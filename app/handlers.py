import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from app.utils import update_task_list, show_tasks, update_scheduled_jobs
from app.db import (find_user_db, create_user_db, clear_tasks_db, 
                    add_reminder_and_task_db, delete_task_db)

# Паттерн для времени в формате '00:00'
time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')

router = Router()
class TaskState(StatesGroup):
    waiting_to_add_task = State()
    waiting_to_add_time = State()
    waiting_to_add_time_input = State()
    waiting_to_add_priority = State()
    waiting_to_delete_task = State()
    waiting_for_confirmation = State()


#Старт
@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    greeting = r'''<b>Добро пожаловать</b>,
<i>Используйте меню ниже для навигации</i>'''

    user_existence = await find_user_db(user_id)

    #Проверка пользователя на существование
    if user_existence is None:
        await create_user_db(user_id, user_name)

    await message.answer(text=greeting, parse_mode='HTML', reply_markup=kb.task_list)


#Отмена действия
@router.message(Command('back'))
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено❌",reply_markup=kb.task_list)
    

#Обработка кнопки списка задач
@router.message(F.text == 'Список задач 📋')
async def handle_show_tasks(message: Message):
    user_id = message.from_user.id

    #Вывод списка задач
    await show_tasks(user_id, message)


#Обработка очистки
@router.callback_query(F.data == 'clear_task')
async def handle_clear_task(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Подтвердите очистку🔄', reply_markup=kb.clear_confirmation)
    await state.set_state(TaskState.waiting_for_confirmation)


#Подтверждение очистки
@router.callback_query(F.data == 'confirm_cleanup', TaskState.waiting_for_confirmation)
async def confirm_delete_task(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    #Очистка данных
    await clear_tasks_db(user_id)

    #Вывод сообщения об очистки
    await callback.message.answer(text=r"<b>Список задач пуст</b>",parse_mode='HTML', reply_markup=kb.task_setting)
    await callback.answer(text='Список очищен')
    await state.clear()


#Обработчик отмены очистки
@router.callback_query(F.data == 'cancel_cleanup')
async def cancel_delete_task(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Очистка отменена.',reply_markup=kb.task_list)
    await state.clear()


#Обработка удаления задачи
@router.callback_query(F.data == 'delete_task')
async def handle_deleting_task(callback: CallbackQuery, state: FSMContext):

    #Установка состояния
    await state.set_state(TaskState.waiting_to_delete_task)
    await callback.message.answer('Введите номер задачи для завершения')


@router.message(TaskState.waiting_to_delete_task)
async def process_delete(message:Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        #Берем номер задачи из списка задач с нумерацией
        user_number = int(message.text)
        data = await update_task_list(user_id)
        
        try:
            to_delete = data[user_number]
        except KeyError:
            await message.answer(text='⚠️*Ошибка:*\n\\-Задача с таким номером не существует\\.',parse_mode='MarkdownV2')
            return
    except ValueError:
        await message.answer(text='⚠️*Ошибка:*\n\\-Номер задачи должен быть числом\\.',
    parse_mode='MarkdownV2')
        return

    #Удаление из базы данных
    await delete_task_db(to_delete)
    await message.answer(text='Задача завершена✅', reply_markup=kb.task_list)
    await state.clear()


#Обработка добавления задачи
@router.callback_query(F.data == 'add_task')
async def handle_add_task(callback: CallbackQuery, state: FSMContext):

    #Установка состояния
    await callback.message.answer(text="Введите название задачи")
    await state.set_state(TaskState.waiting_to_add_task)


@router.message(TaskState.waiting_to_add_task)
async def process_add_task(message: Message, state: FSMContext):
    user_text = message.text

    if len(user_text) < 25:
        # Сохраняем задачу в state
        await state.update_data(user_text=user_text)
        await message.reply(text='<b>Хотите установить напоминание?⏰</b>',parse_mode='HTML',reply_markup=kb.task_reminder)
        await state.set_state(TaskState.waiting_to_add_time)
    else:
        await message.answer(text="⚠️*Ошибка:*\n\\-Пожалуйста, сократите длину задачи до 20 символов\\.", parse_mode="MarkdownV2")
        return


@router.callback_query(F.data == 'no_reminder', TaskState.waiting_to_add_time)
async def handle_no_reminder(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    user_task = data.get('user_text')

    await add_reminder_and_task_db(user_id, user_task)
    await update_task_list(user_id)
    await callback.message.answer(text='Задача добавлена✅')
    await state.clear()

@router.callback_query(F.data == 'yes_reminder', TaskState.waiting_to_add_time)
async def handle_yes_reminder(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.waiting_to_add_time_input)
    await callback.message.answer(text='⏳Введите время для напоминания\n<b>В формате: 00:00</b>',parse_mode='HTML')


@router.message(TaskState.waiting_to_add_time_input)
async def add_reminder_and_task(message: Message, state: FSMContext): 
    user_id = message.from_user.id
    data = await state.get_data()
    user_text = data.get('user_text')
    user_time = message.text
        
    #Проверка времени на правильность формата
    if time_pattern.match(user_time):
        await add_reminder_and_task_db(user_id, user_text, user_time)
        await update_task_list(user_id)

        # Обновляем расписание уведомлений
        from run import bot
        await update_scheduled_jobs(bot,send_notification)

        await message.answer(text='Задача добавлена✅')
        await state.clear()
    else:
        await message.answer(text='⚠️*Ошибка:*\n\\-Пожалуйста, введите время в формате: 00:00\\.', parse_mode='MarkdownV2')
        

#Уведоление пользователю о его задаче
async def send_notification(bot, user_id, task, reminder_time):
    await bot.send_message(user_id, text=f'❗Напоминание.\n<b>{task} — {reminder_time}</b>', parse_mode='HTML')


#Вслучае неизвестной команды
@router.message()
async def unknown_text(message: Message):
    await message.answer("⚠️Неизвестная команда!")


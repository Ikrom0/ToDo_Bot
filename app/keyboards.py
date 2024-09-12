from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                            InlineKeyboardButton, InlineKeyboardMarkup)


task_list = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Список задач 📋')]
],resize_keyboard=True)

task_setting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='добавить🔼',callback_data='add_task'),
    InlineKeyboardButton(text='завершить🔽',callback_data='delete_task')],
    [InlineKeyboardButton(text='очистить🔄', callback_data='clear_task')]
])

task_reminder = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да',callback_data='yes_reminder'), InlineKeyboardButton(text='Нет', callback_data='no_reminder')]
])

clear_confirmation = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Очистить✅", callback_data="confirm_cleanup"),
        InlineKeyboardButton(text="Отмена❌", callback_data="cancel_cleanup")
    ]
])


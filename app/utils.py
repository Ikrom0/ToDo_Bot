from typing import Dict

from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import app.keyboards as kb
from app.db import fetch_tasks_db, fetch_data_for_notification_db


scheduler = AsyncIOScheduler()

async def update_task_list(user_id: int) -> Dict:
    """Эта функция даёт нам возможность сопоставить номер задачи и его айди для того чтобы у нас была возможность удалить задачу по номеру"""

    current_tasks = await fetch_tasks_db(user_id)
    task_number_mapping = {num: task[2] for num, task in enumerate(current_tasks, 1)}
    return task_number_mapping

async def show_tasks(user_id: int, message: Message):
    """Отображение списка задач пользователю."""
    user_tasks = await fetch_tasks_db(user_id)

    if user_tasks == []:
        await message.answer(text=r"<b>Список задач пуст</b>", parse_mode='HTML', reply_markup=kb.task_setting)
    else:
        task_lst = []
        for num, task in enumerate(user_tasks, 1):
            if task[1] is None:
                task_lst.append(f"{num}. <i>{task[0]}</i>")
            else:
                task_lst.append(f"{num}. <i>{task[0]}</i> — <code>{task[1]}</code>")
        task_str = '\n'.join(task_lst)
        await message.answer(text=f"<b>Cписок задач📝\n</b>\n{task_str}", parse_mode='HTML', reply_markup=kb.task_setting)


async def update_scheduled_jobs(bot, send_notification):
    # Удаляем все старые задания
    scheduler.remove_all_jobs()

    # Добавляем новые задачи
    data = await fetch_data_for_notification_db()
    for user_id, task, reminder_time in data:
        hour, minute = map(int, reminder_time.split(':'))
        scheduler.add_job(
            send_notification,
            CronTrigger(hour=hour, minute=minute),
            args=[bot, user_id, task, reminder_time]
        )

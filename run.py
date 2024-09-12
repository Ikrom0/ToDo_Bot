from aiogram import Bot, Dispatcher
import asyncio
import json
import logging

from app.utils import scheduler, update_scheduled_jobs
from app.handlers import router, send_notification

logging.basicConfig(
    filename='bot_errors.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

with open(r'app/config.json') as config_file:
    config = json.load(config_file)

TOKEN = config['TOKEN']
bot = Bot(TOKEN)
dp = Dispatcher()

async def main():
    # Обновление расписания задач при запуске
    await update_scheduled_jobs(bot, send_notification)

    # Запуск планировщика
    scheduler.start()

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print('Бот запущен')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот закрыт')

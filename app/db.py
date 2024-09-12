import aiosqlite
import logging

# Настройка логирования для вывода ошибок
logging.basicConfig(level=logging.ERROR)

async def connect_to_db():
    try:
        return await aiosqlite.connect(r'app\database.db')
    except Exception as e:
        logging.error(f"Ошибка при подключении к базе данных: {e}")
        return None

async def find_user_db(user_id):
    conn = await connect_to_db()
    if not conn:
        return None
    try:
        async with conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)) as cursor:
            return await cursor.fetchone()
    except Exception as e:
        logging.error(f"Ошибка при поиске пользователя: {e}")
        return None
    finally:
        await conn.close()

async def create_user_db(user_id, user_name):
    conn = await connect_to_db()
    if not conn:
        return
    try:
        await conn.execute("INSERT INTO users(user_id, name) VALUES(?,?)", (user_id, user_name))
        await conn.commit()
    except Exception as e:
        logging.error(f"Ошибка при создании пользователя: {e}")
    finally:
        await conn.close()

async def fetch_tasks_db(user_id):
    conn = await connect_to_db()
    if not conn:
        return []
    try:
        async with conn.execute("SELECT task, reminder_time, id FROM tasks WHERE user_id = ?", (user_id, )) as cursor:
            return await cursor.fetchall()
    except Exception as e:
        logging.error(f"Ошибка при получении задач: {e}")
        return []
    finally:
        await conn.close()

async def fetch_data_for_notification_db():
    conn = await connect_to_db()
    if not conn:
        return []
    try:
        async with conn.execute("SELECT user_id, task, reminder_time FROM tasks WHERE reminder_time IS NOT NULL") as cursor:
            return await cursor.fetchall()
    except Exception as e:
        logging.error(f"Ошибка при получении данных для уведомлений: {e}")
        return []
    finally:
        await conn.close()

async def clear_tasks_db(user_id):
    conn = await connect_to_db()
    if not conn:
        return
    try:
        await conn.execute("DELETE FROM tasks WHERE user_id = ?", (user_id,))
        await conn.commit()
    except Exception as e:
        logging.error(f"Ошибка при очистке задач: {e}")
    finally:
        await conn.close()

async def delete_task_db(id):
    conn = await connect_to_db()
    if not conn:
        return
    try:
        await conn.execute("DELETE FROM tasks WHERE id=?", (id,))
        await conn.commit()
    except Exception as e:
        logging.error(f"Ошибка при удалении задачи: {e}")
    finally:
        await conn.close()

async def add_reminder_and_task_db(user_id, task, time=None):
    conn = await connect_to_db()
    if not conn:
        return
    try:
        await conn.execute("INSERT INTO tasks(user_id, task, reminder_time) VALUES(?,?,?);", (user_id, task, time))
        await conn.commit()
    except Exception as e:
        logging.error(f"Ошибка при добавлении задачи и напоминания: {e}")
    finally:
        await conn.close()

<p align="center">
    <img src="https://cdn-aicin.nitrocdn.com/HIAjYmsdLpRQdKpIMJLXFmZsSAYnEnkl/assets/images/optimized/rev-86c0feb/www.amitree.com/wp-content/uploads/2021/08/the-pros-and-cons-of-paper-to-do-lists.jpeg" alt="My Image" width="600" height="300"/>
</p>

<p align="center" style="font-weight: bold;">
    ToDo Bot is a simple and efficient task management bot designed to help users organize their tasks and deadlines with ease.
</p>

## Features
- 📋 **Add Tasks**: Easily create tasks with deadlines to keep track of your schedule.
- ⏰ **Reminders**: Receive timely reminders so you never miss a task.
- 📜 **Task List**: View your task list anytime with a single command.
- ✅ **Task Management**: Mark tasks as completed or delete them when no longer needed.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/todo-bot.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Create a config.json file in the app directory with your Telegram bot token:
   ```python
   {"token": "your-telegram-bot-token"}
4. Set up the database:Ensure you have SQLite installed. Create the required tables in the database. You can use the following SQL commands to set up your database schema:
   ```sqlite
   -- Create the users table
   CREATE TABLE users (
    user_id INTEGER,
    name VARCHAR(100));

   -- Create the tasks table
   CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    time TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (user_id));
6. Run the bot:
   ```bash
   python run.py

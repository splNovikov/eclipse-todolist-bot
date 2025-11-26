from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from database import Database

router = Router()
db = Database()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command."""
    welcome_text = (
        "👋 Привет! Я твой личный todo-list бот.\n\n"
        "📝 Доступные команды:\n"
        "/add <текст> - Добавить задачу\n"
        "/list - Показать все задачи\n"
        "/done <id> - Отметить задачу выполненной\n"
        "/delete <id> - Удалить задачу\n"
        "/clear - Очистить выполненные задачи\n\n"
        "Начни с команды /add, чтобы добавить свою первую задачу!"
    )
    await message.answer(welcome_text)


@router.message(Command("add"))
async def cmd_add(message: Message):
    """Handle /add command to add a new task."""
    # Extract task text after the command
    task_text = message.text.split(maxsplit=1)
    
    if len(task_text) < 2 or not task_text[1].strip():
        await message.answer("❌ Пожалуйста, укажите текст задачи.\nПример: /add Купить молоко")
        return
    
    task_id = await db.add_task(message.from_user.id, task_text[1].strip())
    await message.answer(f"✅ Задача #{task_id} добавлена!")


@router.message(Command("list"))
async def cmd_list(message: Message):
    """Handle /list command to show all tasks."""
    tasks = await db.get_tasks(message.from_user.id)
    
    if not tasks:
        await message.answer("📝 У вас пока нет задач.\nИспользуйте /add чтобы добавить новую задачу.")
        return
    
    # Format tasks list
    response = "📋 Ваши задачи:\n\n"
    for task in tasks:
        status = "✅" if task["completed"] else "⏳"
        response += f"{status} #{task['id']}: {task['text']}\n"
    
    await message.answer(response)


@router.message(Command("done"))
async def cmd_done(message: Message):
    """Handle /done command to mark a task as completed."""
    # Extract task ID
    parts = message.text.split()
    
    if len(parts) < 2:
        await message.answer("❌ Укажите ID задачи.\nПример: /done 1")
        return
    
    try:
        task_id = int(parts[1])
    except ValueError:
        await message.answer("❌ ID задачи должен быть числом.\nПример: /done 1")
        return
    
    # Check if task exists
    task = await db.get_task(message.from_user.id, task_id)
    if not task:
        await message.answer(f"❌ Задача #{task_id} не найдена.")
        return
    
    if task["completed"]:
        await message.answer(f"ℹ️ Задача #{task_id} уже выполнена.")
        return
    
    # Mark as completed
    await db.complete_task(message.from_user.id, task_id)
    await message.answer(f"✅ Задача #{task_id} отмечена выполненной!")


@router.message(Command("delete"))
async def cmd_delete(message: Message):
    """Handle /delete command to delete a task."""
    # Extract task ID
    parts = message.text.split()
    
    if len(parts) < 2:
        await message.answer("❌ Укажите ID задачи.\nПример: /delete 1")
        return
    
    try:
        task_id = int(parts[1])
    except ValueError:
        await message.answer("❌ ID задачи должен быть числом.\nПример: /delete 1")
        return
    
    # Delete task
    success = await db.delete_task(message.from_user.id, task_id)
    
    if success:
        await message.answer(f"🗑 Задача #{task_id} удалена.")
    else:
        await message.answer(f"❌ Задача #{task_id} не найдена.")


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    """Handle /clear command to delete all completed tasks."""
    count = await db.clear_completed(message.from_user.id)
    
    if count > 0:
        await message.answer(f"🗑 Удалено {count} выполненных задач.")
    else:
        await message.answer("ℹ️ Нет выполненных задач для удаления.")

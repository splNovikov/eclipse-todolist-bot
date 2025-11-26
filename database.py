import aiosqlite
from datetime import datetime
from typing import List, Optional


class Database:
    def __init__(self, db_path: str = "/data/todolist.db"):
        self.db_path = db_path

    async def init_db(self):
        """Initialize database and create tables if they don't exist."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    completed_at TEXT
                )
            """)
            await db.commit()

    async def add_task(self, user_id: int, text: str) -> int:
        """Add a new task and return its ID."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO tasks (user_id, text, created_at) VALUES (?, ?, ?)",
                (user_id, text, datetime.now().isoformat())
            )
            await db.commit()
            return cursor.lastrowid

    async def get_tasks(self, user_id: int) -> List[dict]:
        """Get all tasks for a user."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def get_task(self, user_id: int, task_id: int) -> Optional[dict]:
        """Get a specific task by ID."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def complete_task(self, user_id: int, task_id: int) -> bool:
        """Mark a task as completed."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "UPDATE tasks SET completed = 1, completed_at = ? WHERE id = ? AND user_id = ?",
                (datetime.now().isoformat(), task_id, user_id)
            )
            await db.commit()
            return cursor.rowcount > 0

    async def delete_task(self, user_id: int, task_id: int) -> bool:
        """Delete a task."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
            await db.commit()
            return cursor.rowcount > 0

    async def clear_completed(self, user_id: int) -> int:
        """Clear all completed tasks and return the number of deleted tasks."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "DELETE FROM tasks WHERE user_id = ? AND completed = 1",
                (user_id,)
            )
            await db.commit()
            return cursor.rowcount

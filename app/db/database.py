import sqlite3
from typing import List, Tuple, Optional
import os


class Database:
    """Database management class for SQLite operations."""

    def __init__(self, db_path: str):
        """
        Initialize database instance.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def connect(self) -> None:
        """Establish database connection."""
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def create_table(self) -> None:
        """Create tasks table if it doesn't exist."""
        if not self.cursor or not self.connection:
            raise RuntimeError("Database connection not established. Call connect() first.")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            priority TEXT NOT NULL DEFAULT 'medium',
            due_date TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.connection.commit()

    def add_task(self, title: str, description: Optional[str] = None,
                 status: str = "pending", priority: str = "medium",
                 due_date: Optional[str] = None, tags: Optional[str] = None) -> int:
        """
        Add a new task.

        Returns:
            Task ID of the inserted record
        """
        if not self.cursor or not self.connection:
            raise RuntimeError("Database connection not established. Call connect() first.")

        self.cursor.execute("""
            INSERT INTO tasks (title, description, status, priority, due_date, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, status, priority, due_date, tags))
        self.connection.commit()
        task_id = self.cursor.lastrowid
        if task_id is None:
            raise RuntimeError("Failed to retrieve inserted task ID.")
        return task_id

    def get_tasks(self, status: Optional[str] = None, priority: Optional[str] = None) -> List[Tuple]:
        """Get all tasks, optionally filtered by status or priority."""
        if not self.cursor or not self.connection:
            raise RuntimeError("Database connection not established. Call connect() first.")

        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)
        if priority:
            query += " AND priority = ?"
            params.append(priority)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_task(self, task_id: int) -> Optional[Tuple]:
        """Get a specific task by ID."""
        if not self.cursor or not self.connection:
            raise RuntimeError("Database connection not established. Call connect() first.")

        self.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return self.cursor.fetchone()

    def update_task(self, task_id: int, **kwargs) -> bool:
        """Update task fields. Returns True if task was updated."""
        if not self.cursor or not self.connection:
            raise RuntimeError("Database connection not established. Call connect() first.")

        allowed_fields = {'title', 'description', 'status', 'priority', 'due_date', 'tags'}
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not update_fields:
            return False

        update_fields['updated_at'] = 'CURRENT_TIMESTAMP'
        set_clause = ", ".join([f"{k} = CURRENT_TIMESTAMP" if k == 'updated_at' else f"{k} = ?"
                               for k in update_fields.keys()])
        params = [v for k, v in update_fields.items() if k != 'updated_at'] + [task_id]

        self.cursor.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", params)
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if task was deleted."""
        if not self.cursor or not self.connection:
            raise RuntimeError("Database connection not established. Call connect() first.")

        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Shared database instance used across the app
db = Database("app/db/sqlite3.db")

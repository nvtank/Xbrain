import sqlite3
from datetime import datetime

from config import SQLITE_DB_PATH


def init_memory_db():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memory_summary (
            session_id TEXT PRIMARY KEY,
            summary TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def save_message(session_id, role, content):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_memory (
            session_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            session_id,
            role,
            content,
            datetime.now(),
        ),
    )

    conn.commit()
    conn.close()


def load_recent_memory(session_id, limit=6):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM chat_memory
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (session_id, limit),
    )

    rows = cursor.fetchall()
    conn.close()

    rows.reverse()

    formatted = []

    for role, content in rows:
        formatted.append(
            f"{role.upper()}: {content}"
        )

    return "\n".join(formatted)

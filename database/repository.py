from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional

from database.connection import get_connection


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT UNIQUE,
                full_name TEXT,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
            );
            """
        )

        _ensure_user_columns(conn)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chats(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages(chat_id)")


def _ensure_user_columns(conn: sqlite3.Connection) -> None:
    rows = conn.execute("PRAGMA table_info(users)").fetchall()
    columns = {row["name"] for row in rows}
    if "email" not in columns:
        conn.execute("ALTER TABLE users ADD COLUMN email TEXT UNIQUE")
    if "full_name" not in columns:
        conn.execute("ALTER TABLE users ADD COLUMN full_name TEXT")


def create_user(username: str, email: str, full_name: str, password_hash: str) -> bool:
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO users (username, email, full_name, password_hash)
                VALUES (?, ?, ?, ?)
                """,
                (username.strip(), email.strip().lower(), full_name.strip(), password_hash),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, username, email, full_name, password_hash
            FROM users WHERE username = ?
            """,
            (username.strip(),),
        ).fetchone()
    return dict(row) if row else None


def create_chat(user_id: int, title: str) -> int:
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO chats (user_id, title) VALUES (?, ?)", (user_id, title))
        return int(cur.lastrowid)


def rename_chat(chat_id: int, user_id: int, title: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE chats SET title = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (title.strip(), chat_id, user_id),
        )


def user_chats(user_id: int) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, created_at, updated_at
            FROM chats
            WHERE user_id = ?
            ORDER BY updated_at DESC, id DESC
            """,
            (user_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def delete_chat(chat_id: int, user_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM chats WHERE id = ? AND user_id = ?", (chat_id, user_id))


def save_message(chat_id: int, role: str, content: str) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content),
        )
        conn.execute("UPDATE chats SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (chat_id,))
        return int(cur.lastrowid)


def load_messages(chat_id: int) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, role, content, created_at
            FROM messages
            WHERE chat_id = ?
            ORDER BY id ASC
            """,
            (chat_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def import_chat_with_messages(user_id: int, title: str, messages: List[Dict[str, str]]) -> int:
    chat_id = create_chat(user_id=user_id, title=title)
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role in {"user", "assistant", "system"} and content.strip():
            save_message(chat_id, role, content)
    return chat_id

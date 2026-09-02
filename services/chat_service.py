from __future__ import annotations

from typing import Dict, List

from database.repository import (
    create_chat,
    delete_chat,
    import_chat_with_messages,
    load_messages,
    rename_chat,
    save_message,
    user_chats,
)
from utils.formatters import make_chat_title
from utils.validators import validate_chat_title


def new_chat(user_id: int, seed_text: str = "") -> int:
    title = make_chat_title(seed_text) if seed_text else "New Chat"
    return create_chat(user_id=user_id, title=title)


def rename_existing_chat(chat_id: int, user_id: int, title: str) -> tuple[bool, str]:
    ok, msg = validate_chat_title(title)
    if not ok:
        return False, msg
    rename_chat(chat_id=chat_id, user_id=user_id, title=title)
    return True, "Chat renamed."


def remove_chat(chat_id: int, user_id: int) -> None:
    delete_chat(chat_id=chat_id, user_id=user_id)


def list_chats(user_id: int) -> List[Dict]:
    return user_chats(user_id=user_id)


def list_messages(chat_id: int) -> List[Dict]:
    return load_messages(chat_id=chat_id)


def append_message(chat_id: int, role: str, content: str) -> int:
    return save_message(chat_id=chat_id, role=role, content=content)


def import_chat_json(user_id: int, payload: Dict) -> int:
    title = payload.get("chat_title", "Imported Chat")
    messages = payload.get("messages", [])
    return import_chat_with_messages(user_id=user_id, title=title, messages=messages)

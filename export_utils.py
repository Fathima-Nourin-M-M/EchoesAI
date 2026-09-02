from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


EXPORT_DIR = Path("exports")


def export_chat_txt(chat_title: str, messages: List[Dict[str, str]]) -> Path:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = "_".join(chat_title.strip().split())[:40] or "chat_export"
    file_path = EXPORT_DIR / f"{safe_name}.txt"
    lines = [f"Chat: {chat_title}", ""]
    for msg in messages:
        lines.append(f"{msg['role'].upper()}: {msg['content']}")
        lines.append("")
    file_path.write_text("\n".join(lines), encoding="utf-8")
    return file_path


def export_chat_json(chat_title: str, messages: List[Dict[str, str]]) -> Path:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = "_".join(chat_title.strip().split())[:40] or "chat_export"
    file_path = EXPORT_DIR / f"{safe_name}.json"
    payload = {"chat_title": chat_title, "messages": messages}
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return file_path

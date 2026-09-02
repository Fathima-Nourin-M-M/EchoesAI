from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


EXPORT_DIR = Path("exports")


def export_chat_txt(chat_title: str, messages: List[Dict[str, str]]) -> Path:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    safe = "_".join(chat_title.split())[:42] or "chat_export"
    path = EXPORT_DIR / f"{safe}.txt"
    lines = [f"Chat: {chat_title}", ""]
    for msg in messages:
        lines.append(f"{msg['role'].upper()}: {msg['content']}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def export_chat_json(chat_title: str, messages: List[Dict[str, str]]) -> Path:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    safe = "_".join(chat_title.split())[:42] or "chat_export"
    path = EXPORT_DIR / f"{safe}.json"
    payload = {"chat_title": chat_title, "messages": messages}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def parse_import_json(raw_bytes: bytes) -> Dict:
    data = json.loads(raw_bytes.decode("utf-8"))
    if not isinstance(data, dict) or "messages" not in data:
        raise ValueError("Invalid JSON format.")
    return data

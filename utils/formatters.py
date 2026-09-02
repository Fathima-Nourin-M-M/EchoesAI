from __future__ import annotations

from datetime import datetime


def make_chat_title(seed_text: str) -> str:
    clean = " ".join(seed_text.strip().split())
    if not clean:
        return f"Chat {datetime.now().strftime('%H:%M')}"
    return clean[:56] + ("..." if len(clean) > 56 else "")


def format_timestamp(timestamp: str) -> str:
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", ""))
        return parsed.strftime("%d %b %H:%M")
    except ValueError:
        return timestamp

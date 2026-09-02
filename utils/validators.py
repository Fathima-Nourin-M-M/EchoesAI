from __future__ import annotations

import re
from typing import Tuple


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_signup_input(
    full_name: str,
    username: str,
    email: str,
    password: str,
    confirm_password: str,
) -> Tuple[bool, str]:
    if len(full_name.strip()) < 3:
        return False, "Full name must be at least 3 characters."
    if len(username.strip()) < 3:
        return False, "Username must be at least 3 characters."
    if not EMAIL_RE.match(email.strip().lower()):
        return False, "Please enter a valid email address."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if password != confirm_password:
        return False, "Passwords do not match."
    return True, ""


def validate_chat_title(title: str) -> Tuple[bool, str]:
    clean = title.strip()
    if not clean:
        return False, "Chat title cannot be empty."
    if len(clean) > 80:
        return False, "Chat title must be 80 characters or less."
    return True, ""

from __future__ import annotations

from typing import Optional, Tuple

import bcrypt

from database import create_user, get_user_by_username


def _hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    return hashed.decode("utf-8")


def _verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_user_account(username: str, password: str) -> Tuple[bool, str]:
    username = username.strip()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    ok = create_user(username=username, password_hash=_hash_password(password))
    if not ok:
        return False, "Username already exists."
    return True, "Account created successfully."


def login_user(username: str, password: str) -> Tuple[bool, Optional[int], str]:
    username = username.strip()
    user = get_user_by_username(username)
    if not user:
        return False, None, "Invalid username or password."

    if not _verify_password(password, user["password_hash"]):
        return False, None, "Invalid username or password."

    return True, int(user["id"]), "Login successful."

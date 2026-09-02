from __future__ import annotations

from typing import Optional, Tuple

import bcrypt

from database.repository import create_user, get_user_by_username
from utils.validators import validate_signup_input


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def _verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def signup(
    full_name: str,
    username: str,
    email: str,
    password: str,
    confirm_password: str,
) -> Tuple[bool, str]:
    ok, message = validate_signup_input(full_name, username, email, password, confirm_password)
    if not ok:
        return False, message
    created = create_user(
        username=username,
        email=email,
        full_name=full_name,
        password_hash=_hash_password(password),
    )
    if not created:
        return False, "Username or email already exists."
    return True, "Account created successfully."


def login(username: str, password: str) -> Tuple[bool, Optional[dict], str]:
    user = get_user_by_username(username)
    if not user:
        return False, None, "Invalid username or password."
    if not _verify_password(password, user["password_hash"]):
        return False, None, "Invalid username or password."
    return True, user, "Login successful."

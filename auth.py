"""
Authentication: register, login, logout, users.json persistence.
"""

import hashlib
import json
import re
from pathlib import Path

import streamlit as st

_BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = _BASE_DIR / "users.json"
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,20}$")


def load_users() -> dict:
    if not USERS_FILE.exists():
        return {"users": {}}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if "users" in data else {"users": {}}
    except (json.JSONDecodeError, OSError):
        return {"users": {}}


def save_users(users_data: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_data, f, indent=4)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def validate_username(username: str) -> tuple[bool, str]:
    username = username.strip()
    if not username:
        return False, "Username cannot be empty."
    if not USERNAME_PATTERN.match(username):
        return False, "Username: 3–20 chars, letters, numbers, underscore only."
    return True, ""


def validate_password(password: str, confirm: str | None = None) -> tuple[bool, str]:
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    if confirm is not None and password != confirm:
        return False, "Passwords do not match."
    return True, ""


def register_user(username: str, password: str) -> tuple[bool, str]:
    ok, msg = validate_username(username)
    if not ok:
        return False, msg
    ok, msg = validate_password(password)
    if not ok:
        return False, msg

    username = username.strip()
    users_data = load_users()
    if username in users_data["users"]:
        return False, "Username already exists. Pick another."

    users_data["users"][username] = {"password": hash_password(password)}
    save_users(users_data)
    return True, "Account created! You can log in now."


def login_user(username: str, password: str) -> tuple[bool, str]:
    if not username.strip():
        return False, "Enter your username."
    if not password:
        return False, "Enter your password."

    username = username.strip()
    users_data = load_users()
    if username not in users_data["users"]:
        return False, "Username not found."
    if users_data["users"][username]["password"] != hash_password(password):
        return False, "Incorrect password."
    return True, "Welcome back!"


def init_session_state() -> None:
    defaults = {
        "authenticated": False,
        "username": None,
        "page": "dashboard",
        "history": [],
        "saved_generations": [],
        "generated_questions": None,
        "current_topic": "",
        "current_difficulty": "Medium",
        "current_q_type": "MCQs",
        "total_questions_count": 0,
        "gen_error": None,
        "gen_success": None,
        # Last form values for "Generate again"
        "last_topic": "",
        "last_difficulty": "Medium",
        "last_num_questions": 5,
        "last_q_type": "MCQs",
        "pending_generate": False,
        "offline_mode": True,
        "use_openai": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def bump_stats(num_questions: int, topic: str) -> None:
    """Update session counters after successful generation."""
    st.session_state.total_questions_count += num_questions
    if topic and topic not in st.session_state.history:
        st.session_state.history.append(topic)


def logout() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()
    st.rerun()

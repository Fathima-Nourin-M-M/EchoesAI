from __future__ import annotations

from typing import Dict, List

import streamlit as st

from components.auth_views import render_auth_screen
from components.sidebar import render_sidebar
from components.styles import inject_global_styles, typing_indicator_html
from database.repository import init_db
from services.auth_service import login, signup
from services.chat_service import (
    append_message,
    import_chat_json,
    list_chats,
    list_messages,
    new_chat,
    remove_chat,
    rename_existing_chat,
)
from services.ollama_service import OllamaConnectionError, build_prompt_messages, stream_response
from utils.chat_io import export_chat_json, export_chat_txt
from utils.constants import DEFAULT_MODELS, DEFAULT_SYSTEM_PROMPT, MAX_UPLOAD_SIZE_BYTES
from utils.formatters import make_chat_title


def ensure_state() -> None:
    defaults = {
        "authenticated": False,
        "user": None,
        "active_chat_id": None,
        "model": DEFAULT_MODELS[0],
        "temperature": 0.25,
        "max_tokens": 256,
        "context_limit": 6,
        "system_prompt": DEFAULT_SYSTEM_PROMPT,
        "stop_generation": False,
        "rename_chat_id": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def on_login(username: str, password: str) -> None:
    ok, user, message = login(username, password)
    if not ok:
        st.error(message)
        return
    st.session_state.authenticated = True
    st.session_state.user = user
    st.toast("Welcome back.")
    st.rerun()


def on_signup(full_name: str, username: str, email: str, password: str, confirm_password: str) -> None:
    ok, message = signup(full_name, username, email, password, confirm_password)
    if ok:
        st.success(message)
        st.toast("Account created. Please log in.")
    else:
        st.error(message)


def on_logout() -> None:
    for key in ["authenticated", "user", "active_chat_id", "rename_chat_id"]:
        st.session_state[key] = None if key != "authenticated" else False
    st.toast("Logged out.")
    st.rerun()


def active_chat_title(chats: List[Dict], chat_id: int | None) -> str:
    for chat in chats:
        if chat["id"] == chat_id:
            return chat["title"]
    return "Chat"


def render_rename_form(user_id: int) -> None:
    if not st.session_state.rename_chat_id:
        return
    with st.form("rename_chat_form"):
        new_title = st.text_input("Rename chat", max_chars=80)
        col1, col2 = st.columns(2)
        if col1.form_submit_button("Save", use_container_width=True):
            ok, msg = rename_existing_chat(st.session_state.rename_chat_id, user_id, new_title)
            if ok:
                st.session_state.rename_chat_id = None
                st.toast("Chat renamed.")
                st.rerun()
            st.error(msg)
        if col2.form_submit_button("Cancel", use_container_width=True):
            st.session_state.rename_chat_id = None
            st.rerun()


def render_chat() -> None:
    user = st.session_state.user
    chats = list_chats(user["id"])

    state = {
        "model": st.session_state.model,
        "temperature": st.session_state.temperature,
        "max_tokens": st.session_state.max_tokens,
        "context_limit": st.session_state.context_limit,
        "system_prompt": st.session_state.system_prompt,
        "active_chat_id": st.session_state.active_chat_id,
    }

    render_sidebar(
        user_label=user.get("full_name") or user["username"],
        chats=chats,
        state=state,
        on_new_chat=lambda: _handle_new_chat(user["id"]),
        on_open_chat=lambda cid: _open_chat(cid),
        on_delete_chat=lambda cid: _delete_chat(cid, user["id"]),
        on_rename_chat=lambda cid: _set_rename_mode(cid),
        on_import_json=lambda payload: _import_chat(payload, user["id"]),
        on_logout=on_logout,
    )

    st.session_state.model = state["model"]
    st.session_state.temperature = state["temperature"]
    st.session_state.max_tokens = state["max_tokens"]
    st.session_state.context_limit = state["context_limit"]
    st.session_state.system_prompt = state["system_prompt"]

    st.title("Self-Hosted AI Platform")
    st.caption("Private local inference with persistent chat memory")

    render_rename_form(user["id"])

    if not st.session_state.active_chat_id:
        st.info("Create a new chat from the sidebar to start.")
        return

    messages = list_messages(st.session_state.active_chat_id)
    rendered_messages: List[Dict[str, str]] = [{"role": m["role"], "content": m["content"]} for m in messages]

    for message in rendered_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    _render_export_actions(chats, rendered_messages)

    prompt = st.chat_input("Message your assistant")
    if prompt is None:
        return
    if not prompt.strip():
        st.warning("Prompt cannot be empty.")
        return

    with st.chat_message("user"):
        st.markdown(prompt)
    append_message(st.session_state.active_chat_id, "user", prompt)

    if not messages:
        rename_existing_chat(st.session_state.active_chat_id, user["id"], make_chat_title(prompt))

    with st.chat_message("assistant"):
        ph = st.empty()
        ph.markdown(typing_indicator_html(), unsafe_allow_html=True)
        answer = ""
        try:
            final_context = build_prompt_messages(
                system_prompt=st.session_state.system_prompt,
                messages=rendered_messages + [{"role": "user", "content": prompt}],
                context_limit=st.session_state.context_limit,
            )
            st.session_state.stop_generation = False
            for token in stream_response(
                model=st.session_state.model,
                messages=final_context,
                temperature=st.session_state.temperature,
                max_tokens=st.session_state.max_tokens,
            ):
                if st.session_state.stop_generation:
                    break
                answer += token
                ph.markdown(answer + "▌")
            ph.markdown(answer if answer else "_Generation stopped._")
        except OllamaConnectionError as exc:
            st.error(str(exc))
            return
        except Exception:
            st.error("Streaming interrupted. Please try again.")
            return

    if answer.strip():
        append_message(st.session_state.active_chat_id, "assistant", answer)
    st.rerun()


def _render_export_actions(chats: List[Dict], messages: List[Dict[str, str]]) -> None:
    title = active_chat_title(chats, st.session_state.active_chat_id)
    col1, col2 = st.columns(2)
    if col1.button("Export TXT", use_container_width=True):
        path = export_chat_txt(title, messages)
        st.toast(f"Saved: {path}")
    if col2.button("Export JSON", use_container_width=True):
        path = export_chat_json(title, messages)
        st.toast(f"Saved: {path}")


def _handle_new_chat(user_id: int) -> None:
    st.session_state.active_chat_id = new_chat(user_id)
    st.rerun()


def _open_chat(chat_id: int) -> None:
    st.session_state.active_chat_id = chat_id
    st.rerun()


def _delete_chat(chat_id: int, user_id: int) -> None:
    remove_chat(chat_id, user_id)
    if st.session_state.active_chat_id == chat_id:
        st.session_state.active_chat_id = None
    st.toast("Chat deleted.")
    st.rerun()


def _set_rename_mode(chat_id: int) -> None:
    st.session_state.rename_chat_id = chat_id
    st.rerun()


def _import_chat(payload: Dict, user_id: int) -> None:
    raw = str(payload).encode("utf-8")
    if len(raw) > MAX_UPLOAD_SIZE_BYTES:
        st.error("Import file is too large.")
        return
    try:
        chat_id = import_chat_json(user_id, payload)
        st.session_state.active_chat_id = chat_id
        st.toast("Chat imported.")
        st.rerun()
    except Exception:
        st.error("Invalid import payload.")


def main() -> None:
    st.set_page_config(page_title="Self-Hosted AI Platform", page_icon=":robot_face:", layout="wide")
    inject_global_styles()
    init_db()
    ensure_state()

    if not st.session_state.authenticated:
        render_auth_screen(on_login=on_login, on_signup=on_signup)
        return

    render_chat()


if __name__ == "__main__":
    main()
    
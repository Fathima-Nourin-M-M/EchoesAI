from __future__ import annotations

import json
from typing import Callable, Dict, List

import psutil
import streamlit as st

from utils.constants import DEFAULT_MODELS, PROMPT_TEMPLATES
from utils.formatters import format_timestamp


def render_sidebar(
    user_label: str,
    chats: List[Dict],
    state: Dict,
    on_new_chat: Callable,
    on_open_chat: Callable,
    on_delete_chat: Callable,
    on_rename_chat: Callable,
    on_import_json: Callable,
    on_logout: Callable,
) -> None:
    st.sidebar.title("Workspace")
    st.sidebar.caption(f"Signed in as `{user_label}`")

    state["model"] = st.sidebar.selectbox("Model", DEFAULT_MODELS, index=DEFAULT_MODELS.index(state["model"]))
    state["temperature"] = st.sidebar.slider("Temperature", 0.0, 1.0, state["temperature"], 0.05)
    state["max_tokens"] = st.sidebar.slider("Max response tokens", 64, 1024, state["max_tokens"], 32)
    state["context_limit"] = st.sidebar.slider("Context window", 2, 20, state["context_limit"])

    selected_template = st.sidebar.selectbox("Prompt template", list(PROMPT_TEMPLATES.keys()))
    if st.sidebar.button("Apply template", use_container_width=True):
        state["system_prompt"] = PROMPT_TEMPLATES[selected_template]
        st.toast("Prompt template applied.")

    state["system_prompt"] = st.sidebar.text_area("System prompt", state["system_prompt"], height=120)

    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    st.sidebar.caption(f"CPU: {cpu:.0f}% | RAM: {ram:.0f}%")
    st.sidebar.divider()

    if st.sidebar.button("New chat", use_container_width=True):
        on_new_chat()
    if st.sidebar.button("Stop generation", use_container_width=True):
        st.session_state.stop_generation = True
        st.toast("Stopping current generation...")

    uploaded = st.sidebar.file_uploader("Import chat JSON", type=["json"])
    if uploaded is not None and st.sidebar.button("Import now", use_container_width=True):
        try:
            payload = json.loads(uploaded.getvalue().decode("utf-8"))
            on_import_json(payload)
        except Exception:
            st.sidebar.error("Invalid import file.")

    st.sidebar.divider()
    st.sidebar.subheader("Chat history")

    for chat in chats:
        is_active = chat["id"] == state["active_chat_id"]
        label = f"{chat['title']}\n{format_timestamp(chat['updated_at'])}"
        cols = st.sidebar.columns([6, 1, 1])
        if cols[0].button(label, key=f"open_{chat['id']}", use_container_width=True, type="primary" if is_active else "secondary"):
            on_open_chat(chat["id"])
        if cols[1].button("R", key=f"rn_{chat['id']}", use_container_width=True):
            on_rename_chat(chat["id"])
        if cols[2].button("X", key=f"del_{chat['id']}", use_container_width=True):
            on_delete_chat(chat["id"])

    st.sidebar.divider()
    if st.sidebar.button("Logout", use_container_width=True):
        on_logout()

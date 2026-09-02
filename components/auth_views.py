from __future__ import annotations

from typing import Callable

import streamlit as st


def render_auth_screen(on_login: Callable, on_signup: Callable) -> None:
    st.title("Local AI Platform")
    st.caption("Self-hosted, private, CPU-friendly assistant")

    tab_login, tab_signup = st.tabs(["Login", "Create account"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                on_login(username, password)

    with tab_signup:
        with st.form("signup_form"):
            full_name = st.text_input("Full name")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            if st.form_submit_button("Create account", use_container_width=True):
                on_signup(full_name, username, email, password, confirm_password)

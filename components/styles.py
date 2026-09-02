from __future__ import annotations

import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.5rem; max-width: 1080px;}
        .stChatMessage {padding-top: 0.3rem; padding-bottom: 0.3rem;}
        .stChatMessage [data-testid="stMarkdownContainer"]{
            max-width: 760px;
            line-height: 1.55;
            font-size: 0.98rem;
        }
        .stChatMessage.user [data-testid="stMarkdownContainer"]{
            background: rgba(77, 107, 254, 0.18);
            border: 1px solid rgba(110, 140, 255, 0.35);
            border-radius: 16px;
            padding: 0.75rem 0.95rem;
            margin-left: auto;
        }
        .stChatMessage.assistant [data-testid="stMarkdownContainer"]{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 0.75rem 0.95rem;
        }
        .typing-dots {
            display: inline-flex; align-items: center; gap: 4px;
            color: #9aa0b8; font-size: 13px;
        }
        .typing-dots span {
            width: 6px; height: 6px; border-radius: 50%;
            background: #9aa0b8; display: inline-block;
            animation: blink 1.2s infinite ease-in-out;
        }
        .typing-dots span:nth-child(2){animation-delay: .2s;}
        .typing-dots span:nth-child(3){animation-delay: .4s;}
        @keyframes blink {
            0%, 80%, 100% {opacity: .2; transform: translateY(0);}
            40% {opacity: 1; transform: translateY(-1px);}
        }
        @media (max-width: 768px) {
            .block-container {padding-left: .75rem; padding-right: .75rem;}
            .stChatMessage [data-testid="stMarkdownContainer"]{max-width: 100%;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def typing_indicator_html() -> str:
    return '<div class="typing-dots"><span></span><span></span><span></span>AI is typing</div>'

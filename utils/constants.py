from __future__ import annotations

DEFAULT_MODELS = ["gemma3:2b", "phi3:mini", "gemma3:4b", "llama3:8b"]

DEFAULT_SYSTEM_PROMPT = (
    "You are a reliable local assistant. "
    "Prioritize factual, grounded responses. "
    "If information is uncertain, say what is unknown and ask clarifying questions. "
    "Do not invent citations, APIs, files, or commands."
)

PROMPT_TEMPLATES = {
    "Balanced Assistant": DEFAULT_SYSTEM_PROMPT,
    "Code Reviewer": (
        "You are a careful code reviewer. "
        "Be explicit about assumptions and mention risks before suggestions."
    ),
    "Summarizer": (
        "You summarize text clearly and briefly. "
        "Avoid speculation and preserve key facts."
    ),
}

MAX_UPLOAD_SIZE_BYTES = 512 * 1024

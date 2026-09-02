from __future__ import annotations

import json
from typing import Dict, Generator, List

import requests


OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
REQUEST_TIMEOUT = 60


class OllamaConnectionError(Exception):
    """Raised when the local Ollama API is unavailable."""


def build_prompt_messages(
    system_prompt: str,
    messages: List[Dict[str, str]],
    context_limit: int,
) -> List[Dict[str, str]]:
    trimmed = messages[-max(context_limit, 1) :]
    final_messages: List[Dict[str, str]] = []
    if system_prompt.strip():
        final_messages.append({"role": "system", "content": system_prompt.strip()})
    final_messages.extend(trimmed)
    return final_messages


def _messages_to_prompt(messages: List[Dict[str, str]]) -> str:
    lines: List[str] = []
    for msg in messages:
        role = msg["role"].strip().upper()
        content = msg["content"].strip()
        lines.append(f"{role}: {content}")
    lines.append("ASSISTANT:")
    return "\n\n".join(lines)


def stream_ollama_response(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float,
    max_tokens: int,
) -> Generator[str, None, None]:
    payload = {
        "model": model,
        "prompt": _messages_to_prompt(messages),
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }

    try:
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json=payload,
            stream=True,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise OllamaConnectionError(
            "Cannot connect to Ollama. Start Ollama first, then retry."
        ) from exc

    if response.status_code != 200:
        raise OllamaConnectionError(
            f"Ollama returned HTTP {response.status_code}. Check model name and server status."
        )

    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            chunk = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "response" in chunk:
            yield chunk["response"]
        if chunk.get("done"):
            break

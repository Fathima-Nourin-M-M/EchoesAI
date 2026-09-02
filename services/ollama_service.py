from __future__ import annotations

import json
from typing import Dict, Generator, List

import requests


OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
REQUEST_TIMEOUT = 90


class OllamaConnectionError(Exception):
    pass


def build_prompt_messages(
    system_prompt: str,
    messages: List[Dict[str, str]],
    context_limit: int,
) -> List[Dict[str, str]]:
    trimmed = messages[-max(context_limit, 1) :]
    payload: List[Dict[str, str]] = []
    if system_prompt.strip():
        payload.append({"role": "system", "content": system_prompt.strip()})
    payload.extend(trimmed)
    return payload


def _as_instruction_prompt(messages: List[Dict[str, str]]) -> str:
    lines: List[str] = []
    for msg in messages:
        role = msg["role"].upper()
        lines.append(f"{role}: {msg['content'].strip()}")
    lines.append("ASSISTANT:")
    return "\n\n".join(lines)


def stream_response(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float,
    max_tokens: int,
) -> Generator[str, None, None]:
    try:
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json={
                "model": model,
                "prompt": _as_instruction_prompt(messages),
                "stream": True,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "num_ctx": 2048,
                },
            },
            stream=True,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise OllamaConnectionError("Ollama is offline. Start Ollama and retry.") from exc

    if response.status_code != 200:
        raise OllamaConnectionError(f"Ollama error: HTTP {response.status_code}")

    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            chunk = json.loads(line)
        except json.JSONDecodeError:
            continue
        token = chunk.get("response")
        if token:
            yield token
        if chunk.get("done"):
            break

# EchoesAI 💬

A lightweight local chatbot with built-in conversation summarization, built using Ollama and Streamlit.

## Overview

A simple, self-contained chatbot that runs entirely locally using Ollama's Phi-3 Mini model — no external API calls, no cloud dependency. Alongside standard chat functionality, it includes conversation summarization, letting users get a quick digest of longer chat sessions instead of scrolling back through the full history.

## Features

- 💬 **Local chat interface** — clean, interactive Streamlit UI for real-time conversation
- 🧠 **Powered by Phi-3 Mini** — runs via Ollama, entirely on local hardware
- 📝 **Conversation summarization** — condenses chat history into a concise summary on demand
- 🔒 **Fully local** — no data leaves your machine; no API keys or external services required

## Tech Stack

- **LLM Runtime**: Ollama
- **Model**: Phi-3 Mini
- **Frontend**: Streamlit

## How It Works

1. Ollama serves the Phi-3 Mini model locally
2. The Streamlit frontend provides a chat interface for sending messages and viewing responses
3. At any point, the user can trigger a summarization of the conversation so far, which the model condenses into a short digest

## Getting Started

**Prerequisites**: [Ollama](https://ollama.ai/) installed locally, with the Phi-3 Mini model pulled:
```bash
ollama pull phi3
```

**Run the app**:
```bash
streamlit run app.py
```

## Status

Core chat and summarization functionality implemented and working.

---

*A small, practical demonstration of running a capable local LLM with a clean interface — no cloud, no API costs.*

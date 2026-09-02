# Self-Hosted AI Platform (Streamlit + Ollama + SQLite)

A lightweight local AI platform with:

- User signup/login/logout with full name + email
- Persistent multi-chat history with rename/delete + timestamps
- Streamed Ollama responses and local model switching
- Import/export chat as JSON/TXT
- Modular production-style architecture

This implementation is optimized for consumer laptops by keeping memory usage low and limiting prompt context.

## Project Structure

```text
chatbot/
  app.py
  services/
    auth_service.py
    chat_service.py
    ollama_service.py
  database/
    connection.py
    repository.py
  components/
    auth_views.py
    sidebar.py
    styles.py
  utils/
    constants.py
    validators.py
    formatters.py
    chat_io.py
  requirements.txt
  data/
  exports/
  assets/
```

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install and run Ollama:
   - Download from [https://ollama.com/download](https://ollama.com/download)
   - Ensure Ollama is running locally on `http://localhost:11434`

4. Pull recommended lightweight models:

   ```bash
   ollama pull phi3:mini
   ollama pull gemma3:2b
   ollama pull gemma3:4b
   ollama pull llama3:8b
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

## Notes

- Optimized defaults for CPU-only laptops:
  - low default temperature
  - short context window controls
  - compact token settings
  - lightweight dependency set

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

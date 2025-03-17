# Notes Management System

This project is a Notes Management System built using FastAPI, SQLAlchemy, and integrated with AI capabilities for note summarization. The application allows users to create, manage, and analyze text notes while leveraging AI for enhanced functionality.

## Features

- Create, read, update, and delete notes.
- Maintain version history for each note.
- Summarize notes using the Gemini API.
- Analyze notes to calculate various statistics, including:
  - Total word count across all notes.
  - Average note length.
  - Most common words or phrases.
  - Top 3 longest and shortest notes.


## Getting Started
### clone the repo

 `git clone https://github.com/FanniMalevych/notes_management`

### create virtual environment, install dependencies, run migrations (do not forget about .env)

`python -m venv venv`
`venv\Scripts\activate (on Windows)`
`source venv/bin/activate (on macOS)`
`pip install -r requirements.txt`
`alembic upgrade head`
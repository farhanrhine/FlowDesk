# FlowDesk

FlowDesk is a clean, modern, and high-performance task management application built with Flask and Vanilla CSS. It features a stunning "Editorial Parchment" design language with full dark mode support, role-based access control, and a dynamic dashboard.

## 🚀 Live URL
[https://flowdesk-production.up.railway.app](https://flowdesk-production.up.railway.app)

## ✨ Features
- **Authentication**: Secure signup/login/logout with Flask-Login and Werkzeug hashing.
- **Project Management**: Create projects, manage team members (Admins/Members), and track project-specific progress.
- **Task Management**: Create, assign, and edit tasks. Real-time status updates via async JSON requests.
- **Role-Based Access Control (RBAC)**: Detailed permission system for project settings and task management.
- **Dynamic Dashboard**: Personalized summary of tasks due today, in-progress work, and overdue alerts.
- **Editorial Parchment Design**: A premium, state-of-the-art UI with responsive layouts and fluid typography.
- **Dark Mode**: Native dark mode support with localStorage persistence.

## 🛠️ Tech Stack
- **Backend**: Flask, SQLAlchemy (ORM)
- **Database**: SQLite (Local), PostgreSQL (Production)
- **Frontend**: Vanilla CSS (Custom Design System), Vanilla JS, Jinja2
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Deployment**: Railway

## 💻 Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/farhanrhine/FlowDesk.git
   cd FlowDesk
   ```

2. **Setup environment variables**:
   Copy `.env-example` to `.env` and adjust the values:
   ```bash
   cp .env-example .env
   ```

3. **Install dependencies and run**:
   Using `uv`:
   ```bash
   uv sync
   uv run flask run
   ```

## 🌍 Environment Variables
- `SECRET_KEY`: A secret key for session encryption.
- `DATABASE_URL`: Connection string for the database (SQLite by default).
- `FLASK_APP`: Set to `main.py`.
- `FLASK_ENV`: `development` or `production`.

## 📜 License
MIT

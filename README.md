# FlowDesk

FlowDesk is a **minimalist, high-performance task management application** built with a **Zero-Framework Frontend philosophy** (Pure HTML, CSS, and Vanilla JS) and a robust Flask backend. It features a stunning "Editorial Parchment" design language with full dark mode support, role-based access control, and a dynamic dashboard.

## 🚀 Live URL
[https://flowdesk.up.railway.app](https://flowdesk.up.railway.app)

## ✨ Features
- **Authentication**: Secure signup/login/logout with Flask-Login and Werkzeug hashing.
- **Project Management**: Create projects, manage team members (Admins/Members), and track project-specific progress.
- **Task Management**: Create, assign, and edit tasks. Real-time status updates via async JSON requests.
- **Role-Based Access Control (RBAC)**: Detailed permission system for project settings and task management.
- **Dynamic Dashboard**: Personalized summary of tasks due today, in-progress work, and overdue alerts.
- **Editorial Parchment Design**: A premium, state-of-the-art UI with responsive layouts and fluid typography.
- **Dark Mode**: Native dark mode support with localStorage persistence.

## 🛠️ Tech Stack
- **Backend**: **Flask (Python)** — A monolithic engine handling Server-Side Rendering (SSR) via Jinja2 and lightweight JSON APIs.
- **Database**: SQLite (Development) and **PostgreSQL (Production)** via SQLAlchemy ORM.
- **Frontend**: **The Pure Vanilla Stack** — Zero frameworks for maximum performance and design control.
  - **No CSS Frameworks**: 100% custom design system using modern CSS Variables, Flexbox, and Grid.
  - **No JS Frameworks**: Zero-dependency Vanilla JavaScript for all DOM interactions and async updates.
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (Next-generation Python packaging).
- **Deployment**: Railway (Automated CI/CD).


## 📁 Project Structure

```text
FlowDesk/
├── app/
│   ├── auth/           # Authentication blueprints & logic
│   ├── dashboard/      # Personalized metrics & team activity
│   ├── projects/       # Project creation & member management
│   ├── tasks/          # Task lifecycle & status updates
│   ├── static/         # Custom CSS & Vanilla JS
│   ├── templates/      # Jinja2 HTML layouts
│   └── models.py       # Database schema (User, Project, Task)
├── main.py             # Application entry point
├── Procfile            # Deployment instructions for Railway
└── pyproject.toml      # Dependency management (uv)
```

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

## 🧪 Demo Credentials

If you want to test the application immediately with pre-populated data (multiple projects, tasks, and overdue metrics), use the following account (local only sqlite):

*   **Email:** `tester@example.com`
*   **Password:** `password123`

---

## 🧪 End-to-End Testing Guide (Walkthrough)

To verify all features and edge cases, follow this exact sequence:

### 🚀 Key Features to Test
- **Authentication**: Secure Signup, Login, and Password Protection.
- **Project & Team Management**: Creating projects and inviting members with specific roles.
- **Task Lifecycle**: Creation, assignment, and real-time status transitions.
- **Dashboard Metrics**: Real-time summary of active, pending, and overdue work.

---

### Step 1: Account Setup
1.  Navigate to `/auth/register`.
2.  Create account: **Username:** `farhan`, **Email:** `farhan@example.com`, **Password:** `password123`.
3.  Log in and verify the Dashboard says "Welcome, farhan".

### Step 2: Project Creation
1.  Click **Projects** in the navbar -> **New Project**.
2.  **Name:** `EcoStore Web Redesign`, **Description:** `Updating the e-commerce site with a modern aesthetic.`.
3.  Click **Create Project**.

### Step 3: Team Collaboration & RBAC (Edge Case)
1.  Open an **Incognito Window** and register a designer: `designer@studio.com`.
2.  In your `farhan` window, go to the project and **Invite** `designer@studio.com` as a **Member**.
3.  **Edge Case Test**: In the `designer` window, try to access the **Project Settings**. Verify that access is denied because only **Admins** can manage settings.

### Step 4: Sprint Planning & Status Updates
1.  Click **Add Task**.
2.  **Title:** `Homepage Wireframes`, **Assigned To:** `farhan`, **Due Date:** *Today*.
3.  Add another task: **Title:** `SEO Audit`, **Due Date:** *Yesterday* (to test the **Overdue** edge case).
4.  Click on a task and change status to **In Progress**. Verify the badge color updates instantly.

### Step 5: Dashboard & Dark Mode
1.  Click **Dashboard** in the navbar.
2.  Verify the metrics show **1 Overdue** task and your active work.
3.  Toggle **Dark Mode** to see the high-contrast "Parchment" UI adapt to the environment.

## 🌍 Deployment (Railway)

To deploy FlowDesk to [Railway](https://railway.app), follow these steps:

1.  **Connect GitHub**: Create a new project on Railway and connect your GitHub repository.
2.  **Add PostgreSQL**: (Optional but recommended) In your Railway project, click **+ Add** and select **Database > PostgreSQL**.
3.  **Environment Variables**: Go to the **Variables** tab of your service and add the following:
    - `FLASK_APP`: `main.py`
    - `DATABASE_URL`: (Automatically provided by Railway if you added PostgreSQL)
    - `SECRET_KEY`: Generate a random string.
    - `FLASK_ENV`: `production`
4.  **Database Migration**: Once deployed, use the Railway CLI or a migration script to initialize the production database tables.
5.  **Build Command**: Railway will automatically detect the `pyproject.toml` and use `uv` to build the app. The `Procfile` ensures it runs with `gunicorn`.


## 📜 License
MIT

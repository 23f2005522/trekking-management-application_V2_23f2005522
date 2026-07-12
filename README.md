# Trekking Management Application V2

Adventure organizations require an efficient system to manage trekking activities involving **Admins**, **Trek Staff**, and **Trekkers**.

This is **Version 2** of the Trekking Management Application, developed using **Flask (Backend)** and **Vue.js (Frontend)**.

---
[V1_GitHub Repository URL](https://github.com/23f2005522/trekking-management-application_23f2005522)
---

# Prerequisites

Install these before starting:

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Backend |
| **Node.js 18+** | Frontend |
| **Redis** | Background jobs (Celery) + live notifications (Flask-SSE) |
| **MailHog** (optional) | Local email testing |

Verify Redis is working:

```powershell
redis-cli ping
```

Expected output: `PONG`

---

# Installation (Windows)

## Step 1: Clone the repository

```bash
git clone https://github.com/23f2005522/trekking-management-application_v2_23f2005522.git
cd trekking-management-application_v2_23f2005522
```

---

# Backend Setup

## Step 2: Navigate to the backend directory

```bash
cd backend
```

## Step 3: Create a virtual environment (recommended)

```bash
python -m venv venv
```

## Step 4: Activate the virtual environment

**Windows PowerShell**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```cmd
venv\Scripts\activate
```

## Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

Includes Flask, Celery, Redis client, and Flask-SSE.

## Step 6: Apply database migrations

```bash
flask db upgrade
```

First time only:

```bash
flask db init
flask db migrate -m "Initial Migration"
flask db upgrade
```

---

# Running the Application

The app needs **multiple terminals** running at the same time. Start them in this order:

```text
1. Redis
2. Flask backend
3. Celery worker
4. Celery Beat
5. MailHog (optional)
6. Vue frontend
```

---

## Terminal 1 — Redis

```powershell
redis-server
```

Redis is used for:

| Redis DB | Purpose |
|----------|---------|
| 0 | Flask-SSE (live notifications) |
| 1 | Celery task queue |
| 2 | Celery task results |

Settings: `backend/config/config.py`

---

## Terminal 2 — Flask Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

Backend URL: `http://127.0.0.1:5000`

> The database is seeded automatically on first run with default users and sample data.

---

## Terminal 3 — Celery Worker

```powershell
cd backend
.\venv\Scripts\Activate.ps1
celery -A celery_worker.celery_app worker --loglevel=info --pool=solo -n worker1@%h
```

Runs background tasks (emails, reports, CSV export). Use **only one** worker at a time.

**Why these extra flags on Windows?**

- **`--pool=solo`** — On Windows, Celery cannot run the normal way (multiple workers in the background). It will crash. `solo` tells Celery: *run one job at a time, in this same terminal*. That works fine on Windows.
- **`-n worker1@%h`** — Gives your worker a name (like `worker1@YourPCName`). If you accidentally open the worker **twice**, both copies might run the same email or export job **two times**. A unique name helps you avoid that — run **only one** worker terminal.

---

## Terminal 4 — Celery Beat (Scheduler)

```powershell
cd backend
.\venv\Scripts\Activate.ps1
celery -A celery_worker.celery_app beat --loglevel=info
```

Scheduled jobs (config in `backend/celery_worker.py`):

| Job | Schedule |
|-----|----------|
| Daily trek alert | 8:00 AM daily |
| Monthly admin report | 9:00 AM on the 1st of each month |

Use **only one** Beat process at a time.

---

## Terminal 5 — MailHog (optional)

For viewing emails locally without a real SMTP server:

```powershell
.\MailHog_windows_amd64.exe
```

| Service | Address |
|---------|---------|
| SMTP | `localhost:1025` |
| Web UI | [http://localhost:8025](http://localhost:8025) |

---

# Frontend Setup

## Step 7: Navigate to the frontend directory

```bash
cd frontend
```

## Step 8: Install dependencies

```bash
npm install
```

## Step 9: Start the development server

```bash
npm run dev
```

Frontend URL: `http://localhost:5173`

---

# Default Seed Data

More users in `backend/db/seed_data.py`.

## Admin

| Email | Password |
|-------|----------|
| `admin@tma.com` | `admin` |

## Trek Staff

| Email | Password |
|-------|----------|
| `dummy_staff@tma.com` | `staff` |

## Trekker

| Email | Password |
|-------|----------|
| `dummy@tma.com` | `trekker` |

---

# Technology Stack

### Backend

- Flask
- Flask SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Flask-SSE
- Celery
- Redis
- SQLite

### Frontend

- Vue 3
- Vue Router
- Pinia
- Axios
- Bootstrap 5
- Bootstrap Icons

---

# Project Structure

```
trekking-management-application_v2_23f2005522
│
├── backend
│   ├── config/              # App config (Redis, MailHog, JWT)
│   ├── db/                  # Database setup + seed data
│   ├── exports/             # Generated CSV files (gitignored)
│   ├── migrations/
│   ├── model/
│   ├── routes/
│   ├── templates/           # Email HTML templates
│   ├── utils/
│   ├── celery_worker.py     # Celery app + Beat schedule
│   ├── tasks.py             # Background tasks
│   ├── main.py
│   └── requirements.txt
│
├── frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── views/
│   │   └── utils/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Troubleshooting (Windows)

| Problem | Fix |
|---------|-----|
| `SpawnPoolWorker` / `PermissionError` | Use `--pool=solo` on the Celery worker |
| `unknown command HELLO` (Redis) | Use `redis>=4.5,<5.0.0` in requirements.txt |
| Duplicate Celery tasks | Kill old celery processes; run only 1 worker + 1 beat |
| Export job stuck on Pending | Start the Celery worker (Terminal 3) |
| No live notification flash | Ensure Redis is running; log out and log in again |
| Emails not showing | Start MailHog; open [http://localhost:8025](http://localhost:8025) |

---

# Notes

- This guide is for **Windows** users.
- Activate the Python virtual environment before running the backend or Celery.
- Start **Redis** before Flask, Celery worker, and Celery Beat.
- Start the Flask backend before the Vue frontend.
- Ensure Python, Node.js, and Redis are installed before setup.

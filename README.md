# Trekking Management Application V2

A full-stack trekking management system for adventure organizations with three roles: **Admin**, **Trek Staff**, and **Trekkers**.

Built with **Flask** (REST API + Celery + Redis + SSE) and **Vue 3** (Pinia + Bootstrap 5).

**V1 repository:** [trekking-management-application_23f2005522](https://github.com/23f2005522/trekking-management-application_23f2005522)

---

## Features

### Admin
- Dashboard with stats and recent activity
- Trek CRUD with **approval workflow** (Pending → Approved → Open)
- Staff management (approve, reject, blacklist, deactivate/reactivate with reason)
- Trekker management (blacklist, deactivate, reactivate)
- **Bookings** — filter/search by trekker, trek, status, payment, date range
- **Export all bookings** as CSV (async via Celery)
- **Reports page** with Chart.js (bookings per month, treks by status)

### Staff
- Dashboard with assigned treks and **treks starting in 7 days**
- Manage assigned trek status and available slots
- View participants; toggle payment or **mark all paid**
- In-app notifications when assigned or reassigned (+ email)

### Trekker
- Browse and filter open treks (Redis-cached listing)
- Book / re-book / cancel treks (auto-close trek when slots hit 0)
- Trek history + **async CSV export**
- Profile management
- **Booking confirmation email** (Celery)

### Cross-cutting
- **In-app notification panel** (bell icon) for all roles
- **SSE live updates** — stores refresh on new events without page reload
- **Celery Beat** — daily trek reminder emails + monthly admin report
- **Email** via MailHog locally (configurable SMTP via `.env`)

---

## Prerequisites

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Backend |
| **Node.js 22+** (or 24+) | Frontend |
| **Redis** | SSE, caching, Celery broker |
| **MailHog** (optional) | Local email testing |

Verify Redis:

```powershell
redis-cli ping
```

Expected: `PONG`

---

## Quick Start (Windows)

### 1. Clone

```bash
git clone https://github.com/23f2005522/trekking-management-application_v2_23f2005522.git
cd trekking-management-application_v2_23f2005522
```

### 2. Backend setup

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Environment file** — copy the example and edit if needed:

```powershell
copy .env.example .env
```

All config is loaded from `backend/.env` via `python-dotenv`. Do **not** commit `.env` to Git.

```powershell
flask db upgrade
```

First time only (if migrations folder is empty):

```powershell
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. Frontend setup

```powershell
cd ..\frontend
npm install
```

### 4. Run the app (6 terminals)

Start in this order:

| # | Service | Command |
|---|---------|---------|
| 1 | **Redis** | `redis-server` |
| 2 | **Flask** | `cd backend` → activate venv → `python main.py` |
| 3 | **Celery worker** | `celery -A celery_worker.celery_app worker --loglevel=info --pool=solo -n worker1@%h` |
| 4 | **Celery Beat** | `celery -A celery_worker.celery_app beat --loglevel=info` |
| 5 | **MailHog** (optional) | `.\MailHog_windows_amd64.exe` |
| 6 | **Vue dev server** | `cd frontend` → `npm run dev` |

| URL | Address |
|-----|---------|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:5000/api |
| Health check | http://127.0.0.1:5000/api/health/ |
| SSE stream | http://127.0.0.1:5000/stream |
| MailHog UI | http://localhost:8025 |

> Database is seeded automatically on startup when `RUN_SEED_ON_STARTUP=true` in `.env`.

---

## Environment Configuration (`.env`)

Location: `backend/.env` (use `backend/.env.example` as template)

| Variable | Description | Local default |
|----------|-------------|---------------|
| `SECRET_KEY` | Flask secret | change in production |
| `JWT_SECRET_KEY` | JWT signing key | change in production |
| `JWT_ACCESS_TOKEN_HOURS` | Token expiry | `3` |
| `RUN_SEED_ON_STARTUP` | Auto-seed dummy users | `true` |
| `SQLALCHEMY_DATABASE_URI` | Database URL | `sqlite:///Trek.db` |
| `REDIS_URL` | SSE + cache | `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | Celery queue | `redis://localhost:6379/1` |
| `CELERY_RESULT_BACKEND` | Celery results | `redis://localhost:6379/2` |
| `SMTP_HOST` / `SMTP_PORT` | Email server | `localhost` / `1025` (MailHog) |
| `CORS_ORIGINS` | Allowed frontend origins | `*` or `http://localhost:5173` |

---

## Default Login Credentials

Defined in `backend/db/seed_data.py`.

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@tma.com` | `admin` |
| Staff | `dummy_staff@tma.com` | `staff` |
| Trekker | `dummy@tma.com` | `trekker` |

Staff must be **approved** before login. Change passwords after deployment.

---

## Celery Tasks

Configured in `backend/celery_worker.py` and `backend/tasks.py`.

| Task | Trigger | Description |
|------|---------|-------------|
| `send_daily_trek_reminder` | Beat: 8:00 AM daily (IST) | Email trekkers about approved/open treks |
| `send_monthly_admin_report` | Beat: 9:00 AM on 30th (IST) | Email monthly stats to admin |
| `export_trekker_history_csv` | On-demand | Trekker history CSV export |
| `export_admin_bookings_csv` | On-demand | Admin all-bookings CSV export |
| `send_booking_confirmation_email` | On-demand | Email after trekker books |

**Windows Celery worker flags:**
- `--pool=solo` — required on Windows (avoids multiprocessing crash)
- `-n worker1@%h` — unique worker name; run **only one** worker

---

## Redis Usage

| Redis DB | Purpose |
|----------|---------|
| 0 | Flask-SSE, Flask-Caching |
| 1 | Celery message broker |
| 2 | Celery task results |

---

## Technology Stack

### Backend
Flask · Flask-SQLAlchemy · Flask-Migrate · Flask-JWT-Extended · Flask-SSE · Flask-Caching · Celery · Redis · SQLite · python-dotenv

### Frontend
Vue 3 · Vue Router · Pinia · Axios · Bootstrap 5 · Bootstrap Icons · Chart.js · Vite

---

## Project Structure

```
trekking-management-application_v2_23f2005522/
│
├── backend/
│   ├── .env.example          # Env template (commit this)
│   ├── .env                  # Local secrets (gitignored — do not commit)
│   ├── config/config.py      # Loads settings from .env
│   ├── db/                   # DB instance + seed_data.py
│   ├── exports/              # Generated CSV files (gitignored)
│   ├── migrations/
│   ├── model/model.py
│   ├── routes/
│   │   ├── admin_routes.py
│   │   ├── auth_routes.py
│   │   ├── health_routes.py
│   │   ├── notification_routes.py
│   │   ├── staff_routes.py
│   │   └── trekker_routes.py
│   ├── templates/            # HTML email templates
│   ├── utils/
│   │   ├── auth_utility.py
│   │   ├── cache_utility.py
│   │   ├── celery_health.py
│   │   ├── email_utils.py
│   │   └── notification_utils.py
│   ├── celery_worker.py
│   ├── tasks.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Modals, NotificationPanel, Loader, etc.
│   │   ├── stores/           # Pinia (admin, staff, trekker, notifications)
│   │   ├── views/            # Role-based pages
│   │   ├── router/
│   │   └── utils/            # axioUtil.js, logout.js
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## API Overview

Base URL: `http://127.0.0.1:5000/api`

| Prefix | Role | Examples |
|--------|------|----------|
| `/auth` | Public | register, login, logout |
| `/admin` | Admin | treks, staffs, trekkers, bookings, report, export |
| `/staff` | Staff | dashboard, treks, participants, payment |
| `/trekker` | Trekker | treks, booktrek, bookings, history, export |
| `/notifications` | All roles | list, mark read, delete |
| `/health` | Public | health check |

Auth: `Authorization: Bearer <JWT>` header on protected routes.

---

## Production Build (Frontend)

```powershell
cd frontend
npm run build
```

Output: `frontend/dist/` — serve with Nginx or any static host. Point API calls to your backend URL.

For deployment checklist, see internal docs in `resource/DEPLOYMENT_GUIDE.md` (local only, not in repo).

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `SpawnPoolWorker` / `PermissionError` | Use `--pool=solo` on Celery worker (Windows) |
| `unknown command HELLO` (Redis) | Use `redis>=4.5,<5.0.0` in requirements.txt |
| Duplicate Celery tasks / email not sent | Kill old celery processes; run only **1 worker + 1 beat** |
| Export stuck on Pending | Start Celery worker; check Redis is running |
| Booking confirmation email missing | Ensure Celery worker is running; check MailHog at :8025 |
| No live notification updates | Start Redis; log out and log in to reconnect SSE |
| CORS errors from frontend | Set `CORS_ORIGINS=http://localhost:5173` in `.env` |
| Config changes not applied | Restart Flask + Celery after editing `.env` |

---

## Notes

- Guide targets **Windows** development; Linux production can use `prefork` pool instead of `solo`.
- Activate the Python venv before running backend or Celery.
- Start **Redis** before Flask, Celery worker, and Celery Beat.
- Never commit `backend/.env` or `backend/instance/Trek.db`.

---

## Author

**Roll No:** 23f2005522 · MAD-II Project · IIT Madras

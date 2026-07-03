# Trekking Management Application V2

Adventure organizations require an efficient system to manage trekking activities involving **Admins**, **Trek Staff**, and **Trekkers**.

This is **Version 2** of the Trekking Management Application, developed using **Flask (Backend)** and **Vue.js (Frontend)**.

## Repository

GitHub Repository:

https://github.com/23f2005522/trekking-management-application_v2_23f2005522

---

# Installation (Windows)

## Step 1: Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/23f2005522/trekking-management-application_v2_23f2005522.git
```

---

## Step 2: Navigate to the project directory

```bash
cd trekking-management-application_v2_23f2005522
```

---

# Backend Setup

## Step 3: Navigate to the backend directory

```bash
cd backend
```

---

## Step 4: Create a virtual environment (Optional but recommended)

```bash
python -m venv venv
```

---

## Step 5: Activate the virtual environment

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
venv\Scripts\activate
```

---

## Step 6: Install the required dependencies

```bash
pip install -r requirements.txt
```

---

## Step 7: Apply database migrations

```bash
flask db upgrade
```

If this is your first time running the project:

```bash
flask db init
flask db migrate -m "Initial Migration"
flask db upgrade
```

---

## Step 8: Start the Flask backend

```bash
python main.py
```

The backend will start at:

```
http://127.0.0.1:5000
```

> **Note**
>
> The application automatically seeds the database with default users and sample data on the first run.

---

# Frontend Setup

Open **another terminal**.

## Step 9: Navigate to the frontend directory

```bash
cd frontend
```

---

## Step 10: Install frontend dependencies

```bash
npm install
```

---

## Step 11: Start the Vue development server

```bash
npm run dev
```

The frontend will start at:

```
http://localhost:5173
```

---

# Default Seed Data

Additional seeded users can be found in:

```
backend/db/seed_data.py
```

## Admin

| Email | Password |
|--------|----------|
| `admin@tma.com` | `admin` |

---

## Trek Staff

| Email | Password |
|--------|----------|
| `dummy_staff@tma.com` | `staff` |

---

## Trekker

| Email | Password |
|--------|----------|
| `dummy@tma.com` | `trekker` |

---

# Technology Stack

### Backend

- Flask
- Flask SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
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
│   ├── config
│   ├── db
│   ├── installer
│   ├── migrations
│   ├── model
│   ├── routes
│   ├── utils
│   ├── main.py
│   └── requirements.txt
│
├── frontend
│   ├── public
│   ├── src
│   ├── utils
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Notes

- This guide is intended for **Windows** users.
- Always activate the Python virtual environment before running the backend.
- Start the Flask backend before running the Vue frontend.
- Ensure Node.js and Python are installed before beginning the setup.
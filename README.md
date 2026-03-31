# Merkez Beauty Center

A website for a beauty center built with Python (FastAPI) and PostgreSQL.

> **Learning the codebase?** See [LEARN.md](LEARN.md) for a guide explaining APIs, Config, HTML/CSS classes, templates, database, and request flow.

## Features

- **Main page** – Homepage with welcome section
- **About Us** – Company information
- **Our Services** – List of beauty and wellness services
- **Contact** – Communication section with a callback request form

Customers can submit a form to request a callback. Submissions are stored in the database.

## Project Structure

```
Merkez/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application & routes
│   ├── models.py         # Pydantic models (forms, API)
│   ├── config.py         # Settings (database URL, etc.)
│   ├── database.py       # Database connection & session
│   ├── db_models.py      # SQLAlchemy ORM models
│   ├── templates/        # Jinja2 HTML templates
│   └── static/           # CSS, images, etc.
├── run.py                # Application entry point
├── requirements.txt
├── .env.example
└── README.md
```

## Prerequisites

- Python 3.10+
- PostgreSQL

## Setup

### 1. Clone and create virtual environment

```bash
cd Merkez
python -m venv .venv
```

### 2. Activate virtual environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database

Connect to PostgreSQL and run:

```sql
CREATE DATABASE merkez;
```

### 5. Configure environment

Copy the example environment file and edit it with your database credentials:

```bash
copy .env.example .env
```

Edit `.env` and set your PostgreSQL connection URL:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/merkez
```

Format: `postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE`

## Run the application

```bash
python run.py
```

The server starts at **http://localhost:8000**

Tables are created automatically on first startup.

## Routes

| Path       | Description                |
|-----------|----------------------------|
| `/`       | Main page                  |
| `/about`  | About Us                   |
| `/services` | Our Services             |
| `/contact` | Contact & callback form  |
| `/callback` | Form submission (POST)   |

## Database

The `callback_requests` table stores customer callback requests:

| Column     | Type        |
|-----------|-------------|
| id        | SERIAL (PK) |
| name      | VARCHAR(100)|
| phone     | VARCHAR(20) |
| email     | VARCHAR(255)|
| message   | TEXT        |
| created_at| TIMESTAMPTZ |

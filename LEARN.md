# Merkez Beauty Center – Developer Learning Guide

A guide for software engineers learning this project. Explains how the pieces fit together.

---

## Table of Contents

1. [How the Web Works: Request → Response](#1-how-the-web-works-request--response)
2. [What is an API?](#2-what-is-an-api)
3. [Project Structure](#3-project-structure)
4. [The Config Class (Settings)](#4-the-config-class-settings)
5. [HTML & CSS: How Classes Change the Website](#5-html--css-how-classes-change-the-website)
6. [Templates: Jinja2 and Template Inheritance](#6-templates-jinja2-and-template-inheritance)
7. [Database: ORM, Models, and Sessions](#7-database-orm-models-and-sessions)
8. [Request Flow: From URL to Database](#8-request-flow-from-url-to-database)
9. [Key Concepts Summary](#9-key-concepts-summary)

---

## 1. How the Web Works: Request → Response

```
User's browser                    Your server (FastAPI)
      |                                    |
      |  GET /about  (HTTP Request)        |
      | ---------------------------------->|
      |                                    |  Run the "about" function
      |                                    |  Load about.html template
      |                                    |  Fill template with data
      |                                    |
      |  HTML page (HTTP Response)         |
      |<----------------------------------|
      |                                    |
   Browser shows the page
```

- **Request:** Browser asks for a resource (e.g. `/about`).
- **Response:** Server sends back HTML, JSON, or another format.
- **HTTP methods:** `GET` (read), `POST` (create/submit), `PUT`, `DELETE`, etc.

In this project, most routes use `GET` for pages and `POST` for the contact form.

---

## 2. What is an API?

**API** = **A**pplication **P**rogramming **I**nterface.

In web terms, an API is a set of endpoints that other programs can call over HTTP.

### Two ways APIs are often used

| Type | Purpose | Example |
|------|---------|---------|
| **REST API** | Returns JSON for apps/mobile | `GET /api/callbacks` → `[{ "name": "Ali", ... }]` |
| **Server-rendered HTML** | Returns full HTML pages for browsers | `GET /about` → full HTML page |

This project mainly uses **server-rendered HTML**. FastAPI can also expose JSON APIs.

### Our routes as an “API”

- `GET /` → Homepage HTML  
- `GET /about` → About page HTML  
- `POST /callback` → Save form data, redirect  
- `GET /admin/adminDashboard` → Admin page HTML  

Each route is effectively one “endpoint” of the application.

---

## 3. Project Structure

```
Merkez/
├── app/
│   ├── main.py          # Routes (URLs) and request handling
│   ├── config.py        # Settings from environment
│   ├── database.py      # DB connection and sessions
│   ├── db_models.py     # Tables (e.g. callback_requests)
│   ├── models.py        # Pydantic models for validation
│   ├── templates/       # HTML templates (Jinja2)
│   └── static/          # CSS, images, etc.
├── run.py               # Entry point
├── requirements.txt     # Python dependencies
└── .env                 # Secrets (not in git)
```

- **main.py:** Defines routes and what happens on each request.
- **config.py:** Loads configuration (e.g. `DATABASE_URL`).
- **database.py:** Connects to PostgreSQL and manages sessions.
- **db_models.py:** Describes tables and columns.
- **templates/:** Reusable HTML with variables and inheritance.

---

## 4. The Config Class (Settings)

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:123456@localhost:5432/merkez"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### What this does

1. **BaseSettings**  
   Loads values from environment variables and `.env` (via Pydantic).

2. **`database_url`**  
   If `DATABASE_URL` exists in `.env` or environment, it is used.  
   Otherwise the default string is used.

3. **`class Config`**  
   Configures how Settings loads data:

   - `env_file = ".env"` → read from `.env`
   - `env_file_encoding = "utf-8"` → file encoding

4. **`settings = Settings()`**  
   Single global instance, used as `from app.config import settings`.

### Why use it?

- Keeps secrets out of code.
- Different settings per environment (dev, prod).
- One place to change DB URL or other config.

### How we use it

```python
from app.config import settings

engine = create_async_engine(settings.database_url, ...)
```

---

## 5. HTML & CSS: How Classes Change the Website

### What are HTML classes?

Classes are labels you put on HTML elements so CSS can style them:

```html
<a href="/" class="logo">Merkez Beauty Center</a>
<button class="btn">Submit</button>
```

- `class="logo"` → this link has the `logo` class.  
- `class="btn"` → this button has the `btn` class.

### What does CSS do with classes?

CSS uses **selectors** to target elements. A leading `.` means “any element with this class”:

```css
/* Selects any element with class="btn" */
.btn {
    padding: 0.75rem 1.5rem;
    background: #2d2d2d;
    color: #fff;
    border-radius: 4px;
}

/* When you hover over .btn, change background */
.btn:hover {
    background: #444;
}
```

### Selector types in this project

| Selector | Meaning | Example |
|----------|---------|---------|
| `.classname` | Element with that class | `.btn`, `.hero` |
| `element` | Tag name | `body`, `nav`, `footer` |
| `parent child` | Child inside parent | `nav a` = links inside `nav` |
| `parent .class` | Element with class inside parent | `nav .logo` |

### Example from our CSS

```css
/* Elements with class="hero" */
.hero {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #f5efe6 0%, #e8d5c4 100%);
}

/* Links inside nav */
nav a {
    color: #e8d5c4;
}

/* Elements with class="logo" inside nav */
nav .logo {
    font-size: 1.25rem;
    font-weight: bold;
}
```

### How it all connects

1. HTML defines structure and assigns classes.  
2. CSS defines style for those classes (and tags).  
3. Browser applies styles and shows the result.

- To change look: adjust CSS.  
- To change structure: adjust HTML.  
- To add new sections: add HTML and optionally new classes in CSS.

---

## 6. Templates: Jinja2 and Template Inheritance

### What is a template?

A template is HTML with placeholders and logic (variables, loops, blocks). Jinja2 fills those placeholders when the page is rendered.

### Base template

`base.html` is the shared layout for most pages:

```html
<!-- base.html -->
<title>{% block title %}Merkez Beauty Center{% endblock %}</title>
<header>...</header>
<main>
    {% block content %}{% endblock %}   <!-- Child pages fill this -->
</main>
<footer>...</footer>
```

- `{% block content %}` defines an empty area.  
- Child templates “extend” the base and fill that block.

### Child template

```html
<!-- index.html -->
{% extends "base.html" %}

{% block title %}Home - Merkez Beauty Center{% endblock %}

{% block content %}
<section class="hero">
    <h1>Welcome to Merkez Beauty Center</h1>
    <p>Your destination for beauty and wellness.</p>
</section>
{% endblock %}
```

- `{% extends "base.html" %}` → use `base.html` as layout.  
- `{% block title %}...` → replace the base `title` block.  
- `{% block content %}...` → replace the base `content` block.

### Passing data from Python to template

```python
return templates.TemplateResponse(
    "admin_dashboard.html",
    {"request": request, "callbacks": callbacks},
)
```

In the template:

```html
{% for cb in callbacks %}
    <td>{{ cb.name }}</td>
    <td>{{ cb.phone }}</td>
{% endfor %}
```

- `{{ variable }}` → output value.
- `{% for ... %}...{% endfor %}` → loop.
- `{% if condition %}...{% endif %}` → conditionals.

---

## 7. Database: ORM, Models, and Sessions

### ORM = Object-Relational Mapping

ORM lets you use Python classes and objects instead of raw SQL. SQLAlchemy maps classes to tables and objects to rows.

### Model (Table definition)

```python
# db_models.py
class CallbackRequest(Base):
    __tablename__ = "callback_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

- Each `Column(...)` is a column in the `callback_requests` table.  
- `primary_key=True` → unique identifier.  
- `nullable=False` → required.  
- `server_default=func.now()` → default value set by the DB.

### Session

A **session** is a temporary workspace for database operations in a request. Changes are applied together and can be committed or rolled back.

```python
session.add(callback)   # Add new row
await session.commit()  # Save to DB
```

- For reads: query through the session.  
- For writes: `add()`, then `commit()` (or `flush()` if needed before commit).

---

## 8. Request Flow: From URL to Database

### Example: Submitting the callback form

1. User fills form and clicks Submit.  
2. Browser sends `POST /callback` with form data.  
3. FastAPI matches the route:

   ```python
   @app.post("/callback")
   async def submit_callback(name=Form(...), phone=Form(...), ...):
   ```

4. FastAPI parses form fields into `name`, `phone`, etc.  
5. `Depends(get_session)` opens a DB session.  
6. Handler creates and saves a row:

   ```python
   callback = CallbackRequestDB(name=name, phone=phone, ...)
   session.add(callback)
   await session.flush()
   ```

7. Handler returns `RedirectResponse(url="/contact?submitted=1")`.  
8. Browser follows the redirect and shows the contact page with a success message.

### Example: Admin dashboard

1. User opens `/admin/adminDashboard`.  
2. `GET` request hits `admin_dashboard`.  
3. `Depends(get_session)` opens a DB session.  
4. Query loads rows:

   ```python
   result = await session.execute(select(CallbackRequestDB).order_by(...))
   rows = result.scalars().all()
   ```

5. Convert rows to simple dicts (before session closes).  
6. Render `admin_dashboard.html` with `callbacks`.  
7. Return HTML response to the browser.

---

## 9. Key Concepts Summary

| Concept | Meaning |
|---------|---------|
| **Route** | URL + HTTP method (e.g. `GET /about`) mapped to a function |
| **Template** | HTML with variables and logic (Jinja2) |
| **ORM** | Use Python objects instead of raw SQL (SQLAlchemy) |
| **Session** | DB workspace for a request; commit or rollback at the end |
| **Config/Settings** | Load config from env/.env (Pydantic Settings) |
| **CSS class** | Label on HTML; CSS selects it with `.classname` |
| **Dependency (Depends)** | Reusable logic FastAPI injects (e.g. DB session) |
| **Request/Response** | HTTP request in, HTTP response out |

---

## Next Steps to Learn More

1. Change CSS for `.hero` or `.btn` and see the effect.
2. Add a new block in `base.html` and fill it in a child template.
3. Add a new route and a simple HTML response.
4. Add a new column to `CallbackRequest` and run a migration.
5. Read [FastAPI docs](https://fastapi.tiangolo.com/) and [SQLAlchemy docs](https://docs.sqlalchemy.org/).

# 💸 Expense Tracker API

A **fully asynchronous** REST API for tracking personal expenses, built with **FastAPI**, **SQLAlchemy (async)**, and **PostgreSQL** (via Supabase).

---

## 🚀 Tech Stack

| Layer | Technology |
| :--- | :--- |
| Framework | FastAPI |
| Database ORM | SQLAlchemy 2.0 (async) |
| DB Driver | asyncpg |
| Database | PostgreSQL (Supabase) |
| Auth | JWT (python-jose) |
| Password Hashing | passlib (bcrypt) |
| Server | Uvicorn |

---

## 📁 Project Structure

```
ExpenseTracker/
├── app/
│   ├── routers/
│   │   ├── auth.py        # Login endpoint
│   │   ├── users.py       # User registration & lookup
│   │   └── expenses.py    # CRUD for expenses
│   ├── config.py          # Environment variable settings
│   ├── database.py        # Async SQLAlchemy engine & session
│   ├── models.py          # SQLAlchemy table models
│   ├── oauth2.py          # JWT creation & verification
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── utils.py           # Password hashing helpers
│   └── static/            # Frontend HTML files
├── main.py                # App entrypoint, router registration
├── requirements.txt
├── .env                   # Your local secrets (never commit this)
└── .env.example           # Template for environment variables
```

---

## ⚙️ Setup

### 1. Clone the repo & create a virtual environment

```bash
git clone <your-repo-url>
cd ExpenseTracker
python -m venv env
```

### 2. Activate the virtual environment

```bash
# Windows
.\env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Open `.env` and set:

```env
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:6543/postgres
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Note:** If using Supabase, use port `6543` (pooler) in your `DATABASE_URL`. The app is already configured to handle PgBouncer prepared statement limitations.

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

Interactive docs: `http://127.0.0.1:8000/docs`

---

## 🔐 Authentication

This API uses **JWT Bearer tokens**.

1. **Register** → `POST /users/`
2. **Login** → `POST /login` — returns an `access_token`
3. **Use the token** → Add `Authorization: Bearer <token>` header to protected routes

---

## 📬 API Endpoints

### Auth
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/login` | Login and receive a JWT token |

### Users
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/users/` | Register a new user | No |
| `GET` | `/users/{id}` | Get user by ID | No |

### Expenses
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `GET` | `/expenses/` | Get all your expenses | ✅ Required |
| `POST` | `/expenses/` | Create a new expense | ✅ Required |
| `GET` | `/expenses/{id}` | Get a specific expense | ✅ Required |
| `PUT` | `/expenses/{id}` | Update an expense | ✅ Required |
| `DELETE` | `/expenses/{id}` | Delete an expense | ✅ Required |

---

## 🗄️ Database

Tables are created automatically on server startup via the `lifespan` handler in `main.py`.

---

## 🔑 Generating a Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

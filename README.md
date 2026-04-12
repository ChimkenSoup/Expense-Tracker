# Expense Tracker

A modern web application for personal expense management with secure authentication and comprehensive CRUD operations. Built with FastAPI and PostgreSQL for optimal performance and scalability.

## Features

- **Secure Authentication**: JWT-based login and registration system with secure password hashing
- **Expense Management**: Full CRUD operations for creating, reading, updating, and deleting expenses
- **Database Integration**: Asynchronous SQLAlchemy operations with PostgreSQL for efficient data handling
- **Modular Architecture**: Clean separation of concerns with organized routers, schemas, models, and utilities
- **Web Interface**: Responsive HTML templates with CSS and JavaScript for seamless user experience

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM with async support
- **PostgreSQL** - Powerful relational database
- **JWT (python-jose)** - Secure token-based authentication
- **Passlib** - Password hashing with bcrypt

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling and responsive design
- **JavaScript** - Interactive client-side functionality

### Database
- **PostgreSQL** - Primary data storage with ACID compliance

## Project Structure

```
ExpenseTracker/
|-- app/
|   |-- __init__.py
|   |-- config.py           # Environment configuration
|   |-- database.py         # Database connection and session management
|   |-- main.py            # Application entry point
|   |-- models.py          # SQLAlchemy database models
|   |-- oauth2.py          # JWT token creation and validation
|   |-- routers/
|   |   |-- __init__.py
|   |   |-- auth.py        # Authentication endpoints
|   |   |-- expenses.py    # Expense CRUD operations
|   |   |-- users.py       # User management
|   |-- schemas.py         # Pydantic models for request/response
|   |-- static/            # CSS, JavaScript, and static assets
|   |-- templates/         # HTML templates
|   |   |-- dashboard.html
|   |   |-- login.html
|   |   |-- signup.html
|   |-- utils.py           # Password hashing utilities
|-- .env.example           # Environment variables template
|-- .gitignore            # Git ignore rules
|-- main.py               # FastAPI application
|-- requirements.txt      # Python dependencies
`-- README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/ChimkenSoup/Expense-Tracker.git
cd ExpenseTracker
```

### 2. Create Virtual Environment
```bash
python -m venv env

# Windows
.\env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/expense_tracker
SECRET_KEY=your_generated_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Set Up Database
Create a PostgreSQL database:
```sql
CREATE DATABASE expense_tracker;
```

### 6. Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://127.0.0.1:8000`

## API Endpoints

### Authentication
- `POST /users/` - Register a new user
- `POST /login` - Authenticate user and receive JWT token

### Expenses
- `GET /expenses/` - Retrieve all expenses for authenticated user
- `POST /expenses/` - Create a new expense
- `GET /expenses/{id}` - Retrieve a specific expense
- `PUT /expenses/{id}` - Update an existing expense
- `DELETE /expenses/{id}` - Delete an expense

### Users
- `GET /users/{id}` - Retrieve user information

### Web Interface
- `GET /` - Login page
- `GET /signup` - Registration page
- `GET /dashboard` - Main expense dashboard

## Screenshots

### Login Interface
Clean and intuitive login form with secure authentication

### Expense Dashboard
Comprehensive overview of expenses with management capabilities

## Future Improvements

- **Data Visualization**: Add charts and graphs for expense analytics
- **Export Functionality**: PDF and CSV export for expense reports
- **Categories & Tags**: Enhanced expense categorization system
- **Mobile Application**: React Native app for on-the-go expense tracking

## Author

Built with by [ChimkenSoup](https://github.com/ChimkenSoup)

---

**Note**: This project uses modern async/await patterns with SQLAlchemy 2.0 for optimal performance and scalability.

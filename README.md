# Python Todo App

A **full-stack Todo list application** built with **FastAPI**, **SQLAlchemy**, and **vanilla JavaScript**.  
This app allows users to **register, log in, and manage personal tasks** with features like pagination, updating, and deleting todos.  

It is designed to be **secure**, **modular**, and **easy to understand**, making it a strong example for portfolios or resumes.

---

## Features

- **User Authentication:** Secure registration and login using JWT tokens.
- **CRUD Operations:** Create, read, update, and delete todos.
- **Pagination:** Display tasks in a paginated table.
- **Dynamic Frontend:** Interactive dashboard using vanilla JavaScript and HTML/CSS.
- **Responsive Notifications:** Real-time user feedback for actions like task creation or deletion.
- **Database Integration:** PostgreSQL with SQLAlchemy ORM for data persistence.
- **Environment Configuration:** Secure management of secrets using `.env` files.

---

## Tech Stack

- **Backend:** Python 3.11+, FastAPI
- **Database:** PostgreSQL, SQLAlchemy ORM
- **Authentication:** OAuth2.0 + JWT (JSON Web Tokens)
- **Frontend:** HTML, CSS, JavaScript
- **Environment Management:** python-dotenv
- **Password Security:** passlib (bcrypt)

---

## Security

- **Passwords** are hashed and salted using **bcrypt** via `passlib`, protecting against brute-force and rainbow table attacks.
- **JWT tokens** are used for authentication and include an **expiration time** to limit token lifetime and improve security.
- Only authenticated users can access their personal todos.

# Clone the repository
git clone https://github.com/yourusername/python_todo_app.git
cd python_todo_app

# Set up a virtual environment (cross-platform)
python -m venv venv
# Activate the environment:
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Then open .env and fill in:
DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, SECRET_KEY

# Run the FastAPI server
uvicorn app.main:app --reload

# FastAPI SQL Project

A lightweight, robust REST API built using **FastAPI**, **SQLAlchemy**, and **Pydantic v2**. This application demonstrates basic CRUD operations connecting to a local **SQLite** database, complete with structural data validation and duplicate checking mechanisms.

## 🚀 Features

- **FastAPI Framework**: Asynchronous, highly performant web routing layer.
- **SQLAlchemy ORM**: Seamless translation between Python objects and SQL queries.
- **Pydantic v2 Structural Validation**: Clean incoming data validation using up-to-date `model_config` attributes.
- **Robust Error Handling**: Prevents database collisions by intercepting duplicate structural IDs or unique constraints (e.g., duplicate emails) early.

---

## 🛠️ Installation & Setup

Follow these steps to get your local development environment running:

### 1. Clone the Repository
```bash
git clone https://github.com
cd fastapi-sql-project
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install fastapi uvicorn sqlalchemy
```

---

## 🏃 Running the Application

Start the local development server using Uvicorn with auto-reload activated:

```bash
python3 -m uvicorn main:app --reload
```

The application will spin up safely at **`http://127.0.0.1:8000`**.

---

## 🧭 API Endpoints Reference

You can interact with the server directly or import these into testing clients like **Postman**:

### 1. Create a New User
*   **Method:** `POST`
*   **URL:** `http://127.0.0`
*   **Headers:** `Content-Type: application/json`
*   **Body (JSON Raw):**
    ```json
    {
      "id": 1,
      "name": "Alex Mercer",
      "email": "alex@example.com"
    }
    ```

### 2. Fetch a User by ID
*   **Method:** `GET`
*   **URL:** `http://127.0.0{user_id}`  *(e.g., `http://127.0.01`)*

---

## 💡 Interactive Documentation

FastAPI auto-generates interactive API docs out of the box. While your local server is actively running, open your web browser and navigate to:

- **Swagger UI Interactive Docs:** [http://127.0.0](http://127.0.0)
- **ReDoc Alternative Docs:** [http://127.0.0](http://127.0.0)

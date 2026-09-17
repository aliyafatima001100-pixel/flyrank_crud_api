from fastapi import FastAPI
import sqlite3


app = FastAPI(title="Task API", version="1.0")

DATABASE = "tasks.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    cursor = connection.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        connection.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Buy groceries", False)
        )

        connection.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Finish assignment", True)
        )

        connection.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Practice Python", False)
        )

    connection.commit()
    connection.close()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
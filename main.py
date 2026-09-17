from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseModel

import sqlite3


app = FastAPI(title="Task API", version="1.0")

DATABASE = "tasks.db"


class Task(BaseModel):
    title: str
    done: bool = False


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


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    connection = get_db_connection()

    cursor = connection.execute(
        "SELECT id, title, done FROM tasks"
    )

    tasks = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return tasks


@app.get("/tasks/{id}")
def get_task(id: int):
    connection = get_db_connection()

    cursor = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (id,)
    )

    task = cursor.fetchone()

    connection.close()

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return dict(task)


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    connection = get_db_connection()

    cursor = connection.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title.strip(), task.done)
    )

    connection.commit()

    new_id = cursor.lastrowid

    connection.close()

    return {
        "id": new_id,
        "title": task.title.strip(),
        "done": task.done
    }


@app.put("/tasks/{id}")
def update_task(id: int, task: Task):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    connection = get_db_connection()

    cursor = connection.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (task.title.strip(), task.done, id)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    connection.close()

    return {
        "id": id,
        "title": task.title.strip(),
        "done": task.done
    }


@app.delete("/tasks/{id}")
def delete_task(id: int):
    connection = get_db_connection()

    cursor = connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    connection.close()

    return {
        "message": "Task deleted successfully"
    }
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import db


app = FastAPI(title="Task API", version="1.0")


class Task(BaseModel):
    title: str
    done: bool = False


@app.on_event("startup")
def startup():
    db.setup_database()


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
def get_tasks(search: str | None = None, done: bool | None = None):
    return db.fetch_tasks(search, done)


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = db.fetch_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "task not found"},
        )
    return task


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    return db.insert_task(task.title.strip(), task.done)


@app.put("/tasks/{id}")
def update_task(id: int, task: Task):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    updated = db.modify_task(id, task.title.strip(), task.done)

    if updated is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return updated


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    if not db.remove_task(id):
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return Response(status_code=204)
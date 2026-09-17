from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish assignment", "done": True},
    {"id": 3, "title": "Practice Python", "done": False}
]

@app.get(
    "/",
    summary="API information",
    description="Displays basic information about the Task API."
)
def api_info():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get(
    "/health",
    summary="Check API health",
    description="Returns the current health status of the API."
)
def health():
    return {"status": "ok"}


@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns every task currently stored in memory."
)
def list_tasks():
    return tasks

@app.get(
    "/tasks/{task_id}",
    summary="Find one task",
    description="Returns a task using its ID, or 404 when it does not exist."
)
def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a task after checking that a title was provided."
)
def add_task(data: dict):
    title = data.get("title")

    if title is None or not str(title).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    next_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": str(title).strip(),
        "done": False
    }

    tasks.append(new_task)

    return new_task

@app.put(
    "/tasks/{task_id}",
    summary="Edit a task",
    description="Changes the title or completion status of a task."
)
def edit_task(task_id: int, data: dict):
    for task in tasks:
        if task["id"] == task_id:

            if "title" in data:
                title = data["title"]

                if not title or not str(title).strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )

                task["title"] = str(title).strip()

            if "done" in data:
                task["done"] = bool(data["done"])

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Remove a task",
    description="Deletes a task by its ID."
)
def remove_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )
# Task API

A small CRUD API built with Python and FastAPI. It allows users to create, view, update, and delete tasks.

## Run the API

Install the required packages:

```bash
pip install fastapi uvicorn
```

Start the server:

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

## Swagger UI

Interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint          | Purpose                |
|--------|-------------------|-------------------------|
| GET    | `/`               | View API information   |
| GET    | `/health`         | Check server status    |
| GET    | `/tasks`          | View all tasks         |
| GET    | `/tasks/{task_id}`| View one task          |
| POST   | `/tasks`          | Create a task           |
| PUT    | `/tasks/{task_id}`| Update a task           |
| DELETE | `/tasks/{task_id}`| Delete a task           |

## Example Request

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Study FastAPI\"}"
```

Expected status:

```
HTTP/1.1 201 Created
```

## Swagger Screenshot

The Swagger UI screenshot is included in this repository as `swagger.png`.

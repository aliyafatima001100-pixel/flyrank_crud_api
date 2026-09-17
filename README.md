# Task API - Assignment 2

A CRUD API built with Python, FastAPI, and SQLite.

## What changed from Assignment 1?

In Assignment 1, tasks were stored in an in-memory Python list.

In Assignment 2, tasks are stored in a SQLite database. This means
the data remains available even when the FastAPI server is restarted.

## Why SQLite?

SQLite was chosen because it is lightweight and does not require a
separate database server. The entire database is stored in one file.

## Database location

The SQLite database is stored as:

`tasks.db`

in the project directory.

The application automatically creates the database and the `tasks`
table when they do not already exist.

Three example tasks are inserted only when the table is empty.

## How to run

Install the required packages:

```bash
pip install fastapi uvicorn
```

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

## Swagger documentation

Open:

```
http://127.0.0.1:8000/docs
```

## API endpoints

| Method | Endpoint      | Description         |
|--------|---------------|----------------------|
| GET    | `/`           | API information     |
| GET    | `/health`     | Check API health    |
| GET    | `/tasks`      | Get all tasks       |
| GET    | `/tasks/{id}` | Get one task        |
| POST   | `/tasks`      | Create a task        |
| PUT    | `/tasks/{id}` | Update a task        |
| DELETE | `/tasks/{id}` | Delete a task        |

## Example SQL query

```sql
SELECT * FROM tasks WHERE done = 1;
```

This query returns all completed tasks.

## SQLite screenshot

A screenshot of the `tasks.db` database, viewed in a SQLite database
browser, is included in this repository as `sqlite-screenshot.png`.

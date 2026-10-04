#The retry loop makes the API wait for the database instead of crashing when both start together in stage 4

import os
import time

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SEED_TASKS = [
    ("Buy groceries", False),
    ("Finish assignment", True),
    ("Practice Python", False),
]


def connect():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set. Copy .env.example to .env first.")
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def _create_and_seed():
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        total = conn.execute("SELECT COUNT(*) AS total FROM tasks").fetchone()["total"]
        if total == 0:
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)", SEED_TASKS
                )


def setup_database(retries=15, delay=2):
    for attempt in range(1, retries + 1):
        try:
            _create_and_seed()
            return
        except psycopg.OperationalError as exc:
            if attempt == retries:
                raise
            print(f"Database not ready (attempt {attempt}/{retries}): {exc}", flush=True)
            time.sleep(delay)

def fetch_tasks(search=None, done=None):
    query = "SELECT * FROM tasks WHERE TRUE"
    params = []
    if done is not None:
        query += " AND done = %s"
        params.append(done)
    if search is not None:
        query += " AND title ILIKE %s"
        params.append(f"%{search}%")
    query += " ORDER BY id"
    with connect() as conn:
        return conn.execute(query, params).fetchall()


def fetch_task(task_id):
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM tasks WHERE id = %s", (task_id,)
        ).fetchone()            
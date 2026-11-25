# Notes API

A REST API for creating, listing, retrieving, updating, and deleting notes. It is built with FastAPI and stores notes in PostgreSQL through SQLAlchemy.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL

## Setup

Install the project dependencies:

```bash
uv sync
```

Set `DATABASE_URL` in a `.env` file in the project root. For example:

```dotenv
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:5432/DATABASE
```

The database must contain a `notes` table with an integer `id` primary key and `title` and `content` columns. One compatible PostgreSQL definition is:

```sql
CREATE TABLE notes (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content VARCHAR(1000) NOT NULL
);
```

## Run

```bash
uv run uvicorn main:app --reload
```

The API is available at <http://127.0.0.1:8000>. Interactive API documentation is at <http://127.0.0.1:8000/docs>.

## Endpoints

| Method | Path | Description | Responses |
| --- | --- | --- | --- |
| `POST` | `/login` | Check the demo credentials and set an HTTP-only session cookie | `200`, `401` |
| `GET` | `/me` | Return the demo user when a valid session cookie is present | `200`, `401` |
| `POST` | `/notes` | Create a note | `201`, `422` |
| `GET` | `/notes` | List notes | `200` |
| `GET` | `/notes/{note_id}` | Retrieve a note | `200`, `404`, `422` |
| `PUT` | `/notes/{note_id}` | Replace a note's title and content | `200`, `404`, `422` |
| `PATCH` | `/notes/{note_id}` | Update a note's title and/or content | `200`, `404`, `422` |
| `DELETE` | `/notes/{note_id}` | Delete a note | `204`, `404`, `422` |

Note titles must be 1–100 characters and content must be 1–1000 characters. Note IDs must be positive integers. The API currently persists only the title and content; image metadata is not stored in the database.

## Demo login

The demo credentials are:

- Username: `admin`
- Password: `password123`

This is a fixed, development-only login and is not suitable for production use. The note endpoints do not currently require authentication.

## Tests

Run the test suite with:

```bash
uv run pytest -q
```

The database check in `db_test.py` requires a reachable PostgreSQL database configured through `DATABASE_URL`.

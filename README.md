# Notes API

A small in-memory notes API built with FastAPI.

## Install
uv sync

## Run
uv run uvicorn main:app --reload

## Endpoints
- POST /login: authenticate the demo user and set an HTTP-only session cookie
- GET /me: return the authenticated demo user
- POST /notes: create a note (201)
- GET /notes: list all notes (200)
- GET /notes/{note_id}: get one note (200, or 404)
- DELETE /notes/{note_id}: delete a note (204, or 404)
- PUT /notes/{note_id}: replace a note (200, 404, or 422)
- PATCH /notes/{note_id}: partially update a note (200, 404, or 422)

Run the demo credentials:
- username: `admin`
- password: `password123`

## Tests
```bash
uv sync
uv run pytest -q
```
## Errors I tested
- Empty content on PUT /notes/{id}: 422, loc = ["body", "content"], type = string_too_short

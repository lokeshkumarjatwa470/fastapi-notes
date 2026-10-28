# Notes API

A small in-memory notes API built with FastAPI.

## Install
uv sync

## Run
uv run uvicorn main:app --reload

## Endpoints
- POST /notes: create a note (201)
- GET /notes: list all notes (200)
- GET /notes/{note_id}: get one note (200, or 404)
- DELETE /notes/{note_id}: delete a note (204, or 404)
- PUT /notes/{note_id}: update a note(200 , 404 , 422)
## Errors I tested
- Empty content on PUT /notes/{id}: 422, loc = ["body", "content"], type = string_too_short

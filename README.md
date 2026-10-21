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

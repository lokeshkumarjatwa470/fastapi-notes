import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine , text

from typing import Annotated
from fastapi import Body, Cookie, FastAPI, HTTPException, Path, Response, status
from pydantic import BaseModel, Field, HttpUrl

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

app = FastAPI(title="Notes API", version="1.0.0")


class Image(BaseModel):
    url: HttpUrl = Field(title="The URL of the image")
    name: str = Field(title="The name of the image")

class NoteCreate(BaseModel):
    title: str = Field(max_length=100, min_length=1)
    content: str = Field(max_length=1000, min_length=1)
    images: list[Image] | None = Field(
        default=None, title="The list of images associated with the note"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "sample note",
                "content": "This is a sample note for jatwa.",
                "images": [
                    {"url": "https://example.com/image1.jpg", "name": "image1"},
                    {"url": "https://example.com/image2.jpg", "name": "image2"},
                ],
            }
        }
    }

class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=100, min_length=1)
    content: str | None = Field(default=None, max_length=1000, min_length=1)
    images: list[Image] | None = None

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class Note(BaseModel):
    id: int = Field(title="The ID of the note")
    title: str = Field(title="The title of the note")
    content: str = Field(title="The content of the note")
    images: list[Image] | None = Field(
        default=None, title="The list of images associated with the note"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "sample note",
                "content": "This is a sample note for kumar.",
                "images": [
                    {"url": "https://example.com/image1.jpg", "name": "image1"},
                    {"url": "https://example.com/image2.jpg", "name": "image2"},
                ],
            }
        }
    }


notes_db : dict[int, dict] = {}

demo_user = {
    "username": "admin",
    "password": "password123",
}

@app.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, response: Response):
    if credentials.model_dump() != demo_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    response.set_cookie(
        key="session_id",
        value="abc123",
        httponly=True,
        samesite="lax",
    )
    return LoginResponse(access_token="demo-token", token_type="bearer")


@app.get("/me")
async def me(session_id: Annotated[str | None, Cookie()] = None):
    if session_id != "abc123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return {"username": demo_user["username"], "session_id": session_id}


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: Annotated[NoteCreate, Body()]):
    with engine.begin() as conn:
        result = conn.execute(
            text("INSERT INTO notes (title , content) VALUES(:title , :content)  RETURNING id , title , content"),
            {"title":note.title , "content" : note.content},
        )
        row = result.fetchone()
    return row


@app.get("/notes", response_model=list[Note])
def list_notes():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id , title , content FROM notes ORDER by id"))

    rows = result.fetchall() 
    return [Note(id  = row.id , title = row.title , content = row.content) for row in rows]
    

@app.get("/notes/{note_id}", response_model=Note)
def get_note(
    note_id: Annotated[int, Path(title="The ID of the note to retrieve", gt=0)]
):

    with engine.connect() as conn :
        result = conn.execute(
            text("SELECT id , title , content FROM notes WHERE id = :id") ,
            {"id" : note_id},
        )

    row = result.fetchone() 
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return Note(
        id=row.id,
        title=row.title,
        content=row.content,
    )


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: Annotated[int, Path(title="The ID of the note to delete", gt=0)]
):
    note = notes_db.get(note_id)
    if note:
        del notes_db[note_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@app.put("/notes/{note_id}", response_model=Note)
async def update_note(
    note_id: Annotated[int, Path(title="The ID of the note to update", gt=0)],
    note: NoteCreate,
):
    existing_note = notes_db.get(note_id)
    if existing_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    notes_db[note_id] = {
        "title": note.title,
        "content": note.content,
        "images": note.images,
    }
    return Note(
        id=note_id, title=note.title, content=note.content, images=note.images
    )

@app.patch("/notes/{note_id}", response_model=Note)
async def patch_note(
    note_id: Annotated[int, Path(title="The ID of the note to update", gt=0)],
    note: NoteUpdate,
):
    existing_note = notes_db.get(note_id)
    if existing_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    updates = note.model_dump(exclude_unset=True)
    existing_note.update(updates)
    return Note(
        id=note_id,
        title=existing_note["title"],
        content=existing_note["content"],
        images=existing_note["images"],
    )
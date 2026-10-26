from fastapi import FastAPI , Path, HTTPException , status 
from typing import Annotated 
from pydantic import BaseModel , Field, HttpUrl  

app = FastAPI()
next_id = 1

class image(BaseModel):
    url : HttpUrl = Field(title="The URL of the image")
    name : str = Field(title="The name of the image")

class NoteCreate(BaseModel):
    title : str = Field( max_length=100 , min_length=1)
    content : str = Field(max_length=1000 , min_length=1)
    images : list[image] | None = Field(default = None , title="The list of images associated with the note")

class Note(BaseModel):
    id : int = Field(title="The ID of the note")
    title : str = Field(title="The title of the note")
    content : str = Field(title="The content of the note")
    images : list[image] | None = Field(default=None, title="The list of images associated with the note")

notes_db = {}

@app.post("/notes" , status_code=status.HTTP_201_CREATED)
async def create_note(note : NoteCreate):
    global next_id
    note_id = next_id
    next_id += 1
    notes_db[note_id] = {"title": note.title, "content": note.content , "images" : note.images}
    new_note = Note(id=note_id, title=note.title, content=note.content, images=note.images)
    return new_note

@app.get("/notes")
async def list_notes():
    return [Note(id=note_id , title=note["title"]  , content=note["content"] , images=note["images"]) for note_id , note in notes_db.items()]
    
@app.get("/notes/{note_id}")
async def get_note(note_id : Annotated[int , Path(title="The ID of the note to retrieve")]):
    note = notes_db.get(note_id)
    if note is None:
        raise HTTPException(status_code=404 , detail="Note not found")
    return Note(id = note_id , title = note["title"] ,content = note["content"], images = note["images"])

@app.delete("/notes/{note_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id : Annotated[int , Path(title="The ID of the note to delete")]):
    note = notes_db.get(note_id)
    if note:
        del notes_db[note_id]
    else: 
        raise HTTPException(status_code=404 , detail="Note not found")

@app.put("/notes/{note_id}")
async def update_note(note_id : Annotated[int , Path(title="The ID of the note to update")] , note : NoteCreate):
    existing_note = notes_db.get(note_id)
    if existing_note is None:
        raise HTTPException(status_code=404 , detail="Note not found")
    notes_db[note_id] = {"title" : note.title , "content" : note.content , "images" : note.images}
    return Note(id=note_id , title=note.title , content=note.content, images=note.images)
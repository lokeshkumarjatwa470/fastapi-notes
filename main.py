from fastapi import Cookie, FastAPI , Path, HTTPException , status , Body , Response
from typing import Annotated 
from pydantic import BaseModel , Field, HttpUrl  

app = FastAPI()
next_id = 1


class image(BaseModel):
    url : HttpUrl = Field(title="The URL of the image" , example="https://example.com/image.jpg")
    name : str = Field(title="The name of the image" , example="image1")

class NoteCreate(BaseModel):
    title : str = Field( max_length=100 , min_length=1)
    content : str = Field(max_length=1000 , min_length=1)
    images : list[image] | None = Field(default = None , title="The list of images associated with the note")

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "title" : "sample note" ,
                "content" : "This is a sample note for jatwa." ,
                "images" : [
                    {
                        "url" : "https://example.com/image1.jpg",
                        "name" : "image1"
                    },
                    {
                        "url" : "https://example.com/image2.jpg",
                        "name" : "image2"  
                    }
                ]
            }
        }
    }

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class Note(BaseModel):
    id : int = Field(title="The ID of the note")
    title : str = Field(title="The title of the note")
    content : str = Field(title="The content of the note")
    images : list[image] | None = Field(default=None, title="The list of images associated with the note")

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "id" : 1,
                "title" : "sample note" ,
                "content" : "This is a sample note for kumar." ,
                "images" : [
                    {
                        "url" : "https://example.com/image1.jpg",
                        "name" : "image1"
                    },
                    {
                        "url" : "https://example.com/image2.jpg",
                        "name" : "image2"  
                    }
                ]
            }
        }
    }

notes_db = {}

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
    response.set_cookie(key="session_id", value="abc123", httponly=True)
    return LoginResponse(access_token="demo-token", token_type="bearer")


@app.get("/me")
async def me(session_id: Annotated[str | None, Cookie()] = None):
    return {"session_id": session_id}

@app.post("/notes" , status_code=status.HTTP_201_CREATED)
async def create_note(note : Annotated[NoteCreate , Body()]):
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
from fastapi import FastAPI , Path, HTTPException , status 
from typing import Annotated 
from pydantic import BaseModel , Field, HttpUrl  


app = FastAPI()
next_id = 1
class image(BaseModel):
    url : HttpUrl = Field(title="The URL of the image")
    name : str = Field(title="The name of the image")



@app.post("/images", status_code=status.HTTP_201_CREATED)
async def create_images(images: list[image]):
    return images


@app.post("/notes" , status_code=status.HTTP_201_CREATED)
async def create_note(note : dict[int , float]):
    return note
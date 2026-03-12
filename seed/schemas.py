from pydantic import BaseModel
from field_types import Username, Password, NoteTitle, NoteContent

class UserCreate(BaseModel):
    username : Username
    password : Password

class UserLogin(BaseModel):
    username : Username
    password : Password

class NoteCreate(BaseModel):
    title : NoteTitle
    content : NoteContent

class NoteOut(BaseModel):
    id : int
    title : NoteTitle
    content : NoteContent

    class Config:
        orm_mode = True
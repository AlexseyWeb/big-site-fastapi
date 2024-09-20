from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass 

class Post(BaseModel):
    id: int 
    title: str 
    content: str 
    # published: bool
    # created_at: datetime

    class Config:
        orm_mode = True 
   

class InfoAboutAPI(BaseModel):
    version: float
    description: str 
    authors: str

class UserCreate(BaseModel):
    email: EmailStr 
    password: str 
    
    class Config:
        orm_mode = True 
    




    
    
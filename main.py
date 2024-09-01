from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None 

my_posts = [{"title": "First post ", "content": "This is a first post on site", "id": 1}, {"title": "Second post", "content": "A second post on site", "id": 2}]

@app.get("/")
async def root():
    return {"message": "Welcome to my api!!"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/posts")
async def create_posts(new_post:Post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": new_post}
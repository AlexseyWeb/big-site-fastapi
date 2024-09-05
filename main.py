from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None 

my_posts = [{"title": "Zero post", "content": "This is Zero Post", "id" : 0},{"title": "First post ", "content": "This is a first post on site", "id": 1}, {"title": "Second post", "content": "A second post on site", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/")
async def root():
    return {"message": "Welcome to my api!!"}

@app.get("/about_me")
async def about_me():
    return {"API":"Developer AlexseyWeb!"}

#CRUD 

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts")
async def create_posts(new_post:Post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": new_post}


@app.get("/post/{id}")
async def get_post(id:int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found!")
    return {"Detail post: ": post}


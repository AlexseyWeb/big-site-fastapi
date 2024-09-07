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

class InfoAboutAPI(BaseModel):
    version: float
    description: str 
    authors: str



my_posts = [{"title": "Zero post", "content": "This is Zero Post", "id" : 0},{"title": "First post ", "content": "This is a first post on site", "id": 1}, {"title": "Second post", "content": "A second post on site", "id": 2}]
info_api = InfoAboutAPI(version=0.1, description="Default API without details", authors="Gusakov Alexsey Alexseevich")



def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        

@app.get("/")
async def root():
    return {"message": "Welcome to my api!!"}

@app.get("/about_me")
async def about_me():
    return {"version_api": info_api.version, "description_api": info_api.description, "authors_api": info_api.authors }

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

@app.put("/post/{id}")
async def update_post(id:int,  response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Post with{id} is not update")
    new_post = my_posts[id]['title'] = "Change post"
    new_post = my_posts[id]["content"] = "Python is Fun!"
    return {"updated_post": new_post}


@app.get("/post/{id}")
async def get_post(id:int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found!")
    return {"Detail post: ": post}


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
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(new_post:Post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": new_post}

@app.put("/post/{id}")
async def update_post(id:int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Post with{id} is not update")
    post_dict = post.dict()
    post_dict["id"] = id 
    my_posts[index] = post_dict
    return {"updated_post": post_dict}


@app.get("/post/{id}")
async def get_post(id:int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found!")
    return {"Detail post: ": post}

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist!")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
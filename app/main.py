from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

#Models for API
class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
   

class InfoAboutAPI(BaseModel):
    version: float
    description: str 
    authors: str

while True:
    try:
        #bad hardcode
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="password123", cursor_factory=RealDictCursor )
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as err:
        print("Database connection is wrong! ", err)
        time.sleep(2)


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

@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"} 


#CRUD 

@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(new_post:Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": "created post!", "new_post": post}

@app.put("/posts/{id}")
async def update_post(id:int, post:Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING * """, (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Post with{id} is not update")
   
    conn.commit()
    return {"data": updated_post}


@app.get("/posts/{id}")
async def get_post(id:int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found!")
    return {"Detail post: ": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING * """, (str(id),))
    delete_post = cursor.fetchone()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with {id}")
    conn.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
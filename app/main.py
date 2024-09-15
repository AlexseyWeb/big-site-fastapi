from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()



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


info_api = schemas.InfoAboutAPI(version=0.1, description="Default API without details", authors="Gusakov Alexsey Alexseevich")

@app.get("/")
async def root():
    return {"message": "Welcome to my api!!"}

@app.get("/about_me")
async def about_me():
    return {"version_api": info_api.version, "description_api": info_api.description, "authors_api": info_api.authors }

#CRUD functions with SqlAlchemy ORM

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return  new_post

@app.put("/posts/{id}")
async def update_post(id:int, post:schemas.PostBase, db: Session=Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING * """, (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    new_post = post_query.first()

    if new_post == None:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Post with{id} is not update")
   
    # conn.commit()
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return  post_query.first()


@app.get("/posts/{id}")
async def get_post(id:int, db: Session= Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found!")
    return  post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING * """, (str(id),))
    # delete_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)

    if  post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with {id}")
    # conn.commit()
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine
from .routers import post, user, auth

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

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my api!!"}


from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return  new_post

@router.put("/{id}")
async def update_post(id:int, post:schemas.PostBase, db: Session=Depends(get_db), get_current_user: int = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    new_post = post_query.first()

    if new_post == None:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Post with{id} is not update")
   
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return  post_query.first()


@router.get("/{id}")
async def get_post(id:int, db: Session= Depends(get_db), get_current_user: int = Depends(get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found!")
    return  post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if  post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with {id}")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
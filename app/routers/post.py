from typing import List, Optional

from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import oauth2

from .. import models, schemas
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # joined on votes table
    post = db \
        .query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == id) \
        .first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f'Not authorized to perform operation')

    return post


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # with join on votes table
    posts = db \
        .query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .limit(limit) \
        .offset(skip) \
        .all()

    return posts


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id {id} doesn't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform operation')

    post_query.delete(synchronize_session=False)

    db.commit()

    return {"status": "success"}


@router.put("/{id}", response_model=schemas.Post, status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id {id} doesn't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform operation')

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Creates a User"""
    # TODO: make sure to give error if user already exists
    user.password = utils.hash_pass(user.password)

    # get user from schema and unpack dictionary
    new_user = models.User(**user.dict())
    db.add(new_user)  # make change
    db.commit()  # save change
    db.refresh(new_user)  # recieve change

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    # there should only be one
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id:{id} doesn\'t exist.')

    return user

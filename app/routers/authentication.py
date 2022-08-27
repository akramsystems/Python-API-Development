from email.policy import HTTP
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, models, utils, database, oauth2

router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Route for user Login Authentication generates an Access Token to be returned to the user"""
    # OAuth2PasswordRequestForm is username and password as property
    # get the username from the database
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    # check if the username exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # check if the password matches the hashed password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Generate an access token for the given user using our secret token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

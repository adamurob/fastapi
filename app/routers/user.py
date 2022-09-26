
import string

from sqlalchemy import String, null
from .. import models, schema, utils
from fastapi import Body, FastAPI, Response,status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session 
from.. database import get_db
from typing import Optional, List

router = APIRouter(
    prefix= "/users",
    tags = ["User"]
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password 

    count_user = db.query(models.User).filter(models.User.email == user.email).count()
    
    if count_user >= 1:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"User exists")
    else: 
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

@router.get("/{id}", response_model= schema.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exist")
    
    return user


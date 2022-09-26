from os import access
from pickle import NONE
from.. import database,models,schema,utils, oauth2
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model = schema.Token)
def login(user_credentails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentails.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    
    if not utils.verfiy(user_credentails.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    

    access_token = oauth2.create_access_token(data = {"User_id":user.id})

    return {"access_token":access_token, "token_type": "bearer"}
    
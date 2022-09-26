from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import date, datetime

#model defination 
class Postbase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(Postbase):
    pass    



class UserCreate(BaseModel):
    email : EmailStr
    password: str

class UserOut(BaseModel):
    id: int 
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class UserLogin(UserCreate):
    email : EmailStr
    password: str

class Post(Postbase):
    id :int 
    created_at : datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int 
    dir: conint(le=1)

class PostOut(BaseModel):
    Post: Post
    Votes: int

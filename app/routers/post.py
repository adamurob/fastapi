
from posixpath import ismount
from pyexpat import model
from unittest import result
from .. import models, schema, utils, oauth2
from fastapi import Body, FastAPI, Response,status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session 
from.. database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix= "/posts",
    tags = ["Post"]
)




#get all the value
@router.get("/", response_model= List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user),
limit: int=10, skip:int = 0, search : Optional[str] = ""):

    #query 
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts 

#Post to create a post
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schema.Post)
def create_post(post:schema.PostCreate, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING
    # *""" , 
    #                    (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# get a particular post 
@router.get("/{id}", response_model= schema.PostOut) 
def getpost(id:int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""select * from posts where id = %s """, (str(id),))
    #post  =  cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail = "id not fouund")
    
    #if ((post.owner_id) != (int(current_user.id))):
    #   raise HTTPException (status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized to perform requested action")
    
    return post

#delete a partular post
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT) 
def delete_post(id:int,  db: Session = Depends(get_db),current_user:int=(Depends(oauth2.get_current_user))):
    #cursor.execute("""Delete from posts where id = %s returning *""",(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    deleted_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = deleted_query.first()

    if deleted_post == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail = "id not fouund")
    
    if ((deleted_post.owner_id) != (int(current_user.id))):
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized to perform requested action")
    
    deleted_query.delete( synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update a post
@router.put("/{id}", status_code= status.HTTP_201_CREATED, response_model= schema.Post)
def update_post(id:int, post:schema.PostCreate ,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""update posts set title = %s, content = %s, published = %s
    #where id = %s returning *""",(post.title, post.content, post.published , str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = update_query.first()

    if updated_post  == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail = "id not fouund")
    

    if updated_post.owner_id != (int(current_user.id)):
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized to perform requested action")
    
    update_query.update(post.dict(), synchronize_session = False)
    #update_query.update(updated_post.dict(), synchronize_session = False)

    db.commit()

    return update_query.first()
    

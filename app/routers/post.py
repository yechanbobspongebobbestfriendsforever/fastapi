from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags=["post"]
)

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db), 
              current_user:int=Depends(oauth2.get_current_user),
              limit:int=10,
              search:Optional[str]=""
              ):

    posts = (
        db.query(
            models.Post, 
            func.count(models.Vote.post_id).label('votes')
        ).join(
            models.Vote,
            models.Post.id == models.Vote.post_id, 
            isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.title.contains(search)
        ).limit(
            limit=limit
        )
    ).all()
    
    return posts

    
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int,
             db:Session=Depends(get_db), 
             current_user:int=Depends(oauth2.get_current_user)):
    
    post = (
        db.query(
            models.Post, 
            func.count(models.Vote.post_id).label('votes')
        ).join(
            models.Vote,
            models.Post.id == models.Vote.post_id, 
            isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.id==id
        ).first()
    )
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'post with id {id} does not exist'
        )
    return post 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate, 
                db:Session=Depends(get_db), 
                current_user:int=Depends(oauth2.get_current_user)):
 
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, 
                db:Session=Depends(get_db), 
                current_user:int=Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'post with id {id} does not exist'
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorize to performan requested action"
        )
    
    post_query.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, 
                post: schemas.PostCreate, 
                db:Session=Depends(get_db), 
                current_user:int=Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    fetched_post = post_query.first()
    
    if fetched_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'post with id {id} does not exist'
        )
        
    if fetched_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorize to performan requested action"
        )
    post_query.update(
        post.dict(), 
        synchronize_session=False
    )
    db.commit()
    return post_query.first()
    
    
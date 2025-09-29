from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import oauth2
from .. import models, schemas
from ..database import get_db
from typing import List, Optional



router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)



# Get all posts
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit:int = 5,skip:int = 0, search:Optional[str] = ""):
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    posts_with_votes = []
    for post, vote_count in results:
        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "published": post.published,
            "created_at": post.created_at,
            "owner_id": post.owner_id,
            "owner": {
                "id": post.owner.id,
                "email": post.owner.email,
                "created_at": post.owner.created_at
            },
            "votes": vote_count
        }
        posts_with_votes.append(post_data)
    
    return posts_with_votes

# Create a post
@router.post("/", response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

# Get a post
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int,db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
   result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
   if not result:
       raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
   
   post, vote_count = result
   post_data = {
       "id": post.id,
       "title": post.title,
       "content": post.content,
       "published": post.published,
       "created_at": post.created_at,
       "owner_id": post.owner_id,
       "owner": {
           "id": post.owner.id,
           "email": post.owner.email,
           "created_at": post.owner.created_at
       },
       "votes": vote_count
   }
   return post_data
   


# Delete a post
@router.delete("/{id}")
def delete_post(id : int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    
    db.delete(post)
    db.commit()


# Update a post
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if not existing_post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first() 
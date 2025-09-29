from .. import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# Create a user

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    user_query = db.query(models.User).filter(models.User.email == user.email).first()
    if user_query:
        raise HTTPException(status_code=400, detail=f"User with email: {user.email} already exists")
    
    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get a user
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id:int, db = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {id} was not found")
    return user


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserResponse

from app.database import get_db
from app.models.userDB import UserDB

from app.utils.security import hash_password

router = APIRouter(prefix = "/users", tags=["Users"])

@router.post("", response_model = UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserDB(
        username = user.username,
        email = user.email,
        password_hash = hash_password(user.password)
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Username or email already exists"
        )
    
    except Exception:
        db.rollback()
        raise
    
    return new_user


@router.get("", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = (db.query(UserDB).all())
    return users


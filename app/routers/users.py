from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserResponse, UserLogin

from app.database import get_db
from app.models.userDB import UserDB

from app.utils.security import hash_password, verify_password

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


@router.post("/login")
async def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = (db.query(UserDB).filter(UserDB.username == user.username).first())
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,       # We don't want: 404 User not found, because that reveals that the username doesn't exist. 
            detail="Incorrect username or password!"        # Instead, we deliberately give the same message we'll use for an incorrect password, This prevents an attacker from easily discovering which usernames exist.
        )

    if not verify_password(user.password, db_user.password_hash):   # we don't simply hash (user.password) and check equality because password hashing uses a random salt, so hashing the same password again produces a different hash, verify_password() is specifically designed to handle this correctly.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,       
            detail="Incorrect username or password!"        
        )
        

@router.get("", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = (db.query(UserDB).all())
    return users


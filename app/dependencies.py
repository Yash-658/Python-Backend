from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.utils.auth import verify_access_token

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.userDB import UserDB

# Scheme = the authentication mechanism being used.
# used to extract JWT token from the autherization header sent by the user in future requests after login~                         
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")       # tokenUrl is supplied just to tell SwaggerUI this is where tokens are generated so it can represent out authenication schema in docs~

def get_current_user (
    token: str = Depends(oauth2_scheme),             # using FastAPI dependency injection, so when we will call get_current_user, fastapi will call it dependencies first~
    db: Session = Depends(get_db)
    ) -> UserDB: 
    
    payload = verify_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid or expired token"
        )
        
    
    user_id = payload.get("sub")
    
    if user_id is None:                                             # A valid signature proves who signed the document and that it wasn't altered, It doesn't guarantee that the document actually contains the information your application needs.
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,  
            detail = "Invalid token"
        )
        
    db_user = db.query(UserDB).filter(UserDB.id == int(user_id)).first()
    
    if db_user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,  
            detail = "User no longer exists~"
        ) 
        
    return db_user
    
    
def require_role(             # A higher order function~
    required_role: str
):
    def role_checker(         # this is like a specialized dependency fxn
        current_user: UserDB = Depends(get_current_user)
    ):
            
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,      # 403 Forbidden→ "I know who you are, but you're not allowed to do this."
                detail="Insufficient permissions"
            )
            
        return current_user
    
    return role_checker
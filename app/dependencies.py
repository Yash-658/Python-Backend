from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.utils.auth import verify_access_token

# Scheme = the authentication mechanism being used.
# used to extract JWT token from the autherization header sent by the user in future requests after login~                         
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")       # tokenUrl is supplied just to tell SwaggerUI this is where tokens are generated so it can represent out authenication schema in docs~

def get_current_user(token: str = Depends(oauth2_scheme)):          # using FastAPI dependency injection, so when we will call get_current_user, fastapi will call it dependencies first~
    payload = verify_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid or expired token"
        )
        
    return payload
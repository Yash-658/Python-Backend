from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
# Removed UserLogin Schema cuz OAuth2PasswordRequestForm is now handling the request form contract for login

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
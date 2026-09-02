# Role: Create and Verify JWTS


from datetime import datetime, timedelta, timezone 

# datetime → gets the current time.
# timedelta → represents a duration, e.g. 30 minutes.
# timezone → lets us work with UTC-aware timestamps.

import jwt, os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY is not set")

def create_access_token(                # data is the information we want inside the JWT payload
    data: dict,
    expires_delta: timedelta = timedelta(minutes=30)
):
    to_encode = data.copy()                      # We make a copy instead of modifying the original dictionary.
    
    expire = datetime.now(timezone.utc) + expires_delta   # By default, expires_delta is set to 30 mins~
    
    to_encode.update({"exp" : expire})
    
    return jwt.encode(            # jwt format -> HEADER.PAYLOAD.SIGNATURE
        to_encode,                # JWT signatures prevent tampering, but they don't prevent impersonation if a valid JWT itself is stolen.
        SECRET_KEY, 
        algorithm=ALGORITHM       # This fxn encodes the payload and generates the complete JWT, including the signature.
    )    
    

def verify_access_token(token: str):    # this fxn returns the payload if JWT matches, else returns none~
    try:
        payload = jwt.decode(           # PyJWT will verify the token's signature using our SECRET_KEY. It will also validate registered claims such as exp, if it fails, it raises an error~
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        return payload
    
    except jwt.InvalidTokenError:
        return None
    
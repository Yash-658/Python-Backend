import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")    

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind = engine)    # creating session factory, now all sessions will be made using this~

def get_db():                       # used for injecting dependencies, so instead of creating a new session everytime manually, we will pass this~
    db = SessionLocal() 

    try:
        yield db                    # yield pauses the function and gives the database session to whoever requested it.

    finally:
        db.close()

class Base(DeclarativeBase):        # Eventually our coding platform will have many models, and they'll all inherit from Base.
    pass
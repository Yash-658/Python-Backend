from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:7974420106#yash@localhost:5432/coding_platform"

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

class ProblemDB(Base):              # it inherits from Base, SQLAlchemy recognizes it as a database model.
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True)   # an int PK, so SQLAlchemy uses DB auto-increment by default
    title: Mapped[str]                                  # Mapped[str] -> This is mapped to a DB column and its Python type is str
    difficulty: Mapped[str]

Base.metadata.create_all(engine)    # "Using this db engine, create all the tables described by my models if they don't already exist."


from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class ProblemDB(Base):              # it inherits from Base, SQLAlchemy recognizes it as a database model.
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True)                 # an int PK, so SQLAlchemy uses DB auto-increment by default
    title: Mapped[str] = mapped_column(nullable=False, unique=True)   # Mapped[str] -> This is mapped to a DB column and its Python type is str
    difficulty: Mapped[str] = mapped_column(nullable=False)
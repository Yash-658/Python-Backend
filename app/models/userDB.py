from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy import String

class UserDB(Base):
    __tablename__ = "users"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    
    email:Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    
    password_hash:Mapped[str] = mapped_column(nullable=False)
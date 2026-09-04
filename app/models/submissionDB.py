from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Text, ForeignKey

from app.database import Base

class SubmissionDB(Base):
    __tablename__ = "submissions"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),                         # means submissions.problem_id must reference an existing problems.id, At the PostgreSQL level, we're creating referential integrity
        nullable= False
    )
    
    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problems.id"),
        nullable=False
    )
    
    code: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    language: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        server_default="pending"
    )
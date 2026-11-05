from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Text, ForeignKey, func, Integer

from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.problemDB import ProblemDB

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
    
    problem: Mapped["ProblemDB"] = relationship(
        back_populates="submissions"
    )
    
    # judge results~
    execution_time: Mapped[float | None] = mapped_column(nullable=True)
    
    memory_used: Mapped[float | None] = mapped_column(nullable=True)
    
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, 
        server_default=func.now()
    )
    
    passed_test_cases: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    total_test_cases: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0"
    )
    
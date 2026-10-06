from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:                   # this is done for preventing a runtime circular import~
    from app.models.testCaseDB import TestCaseDB
    from app.models.submissionDB import SubmissionDB

class ProblemDB(Base):              # it inherits from Base, SQLAlchemy recognizes it as a database model.
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True)                 # an int PK, so SQLAlchemy uses DB auto-increment by default
    title: Mapped[str] = mapped_column(nullable=False, unique=True)   # Mapped[str] -> This is mapped to a DB column and its Python type is str
    difficulty: Mapped[str] = mapped_column(nullable=False)
    test_cases: Mapped[list["TestCaseDB"]] = relationship(            # ORM relationships let us navigate between related models directly (problem.test_cases / testcase.problem) instead of manually querying each relationship.
    back_populates="problem",                                         # Problem → its test cases (one-to-many ORM relationship).
    cascade="all, delete-orphan"
    )
    
    submissions: Mapped[list["SubmissionDB"]] = relationship(
    back_populates="problem"
    )
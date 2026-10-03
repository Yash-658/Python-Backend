from app.database import Base
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

class TestCaseDB(Base):
    __tablename__ = "test_cases"
    
    id: Mapped[int] = mapped_column(primary_key= True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"), nullable = False)
    input_data: Mapped[str] = mapped_column(Text,nullable=False)
    expected_output: Mapped[str] = mapped_column(Text,nullable=False)
    
    
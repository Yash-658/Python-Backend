from pydantic import BaseModel
from datetime import datetime

class SubmissionCreate(BaseModel):         # user_id I can fetch from the payload~
    problem_id: int
    code: str
    language: str
    
class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    code: str
    language: str
    status: str
    execution_time: float | None
    memory_used: float | None
    error_message: str | None
    created_at: datetime
    passed_test_cases: int
    total_test_cases: int
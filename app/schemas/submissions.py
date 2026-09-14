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
    created_at: datetime
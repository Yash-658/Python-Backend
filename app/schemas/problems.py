from pydantic import BaseModel    # FastAPI uses Pydantic heavily for validating and structuring incoming data.
from app.schemas.testCases import TestCaseCreate


class Problem(BaseModel):         # data validation model (response model)
    id: int
    title: str
    difficulty: str

class ProblemCreate(BaseModel):     # data validation model  (@POST/problems)(request model)
    title: str      
    difficulty: str
    test_cases: list[TestCaseCreate]

class ProblemUpdate(BaseModel):     # data validation model (@PATCH/problems)(request model)
    title: str| None = None
    difficulty: str| None = None
    

from pydantic import BaseModel

class TestCaseCreate(BaseModel):
    input_data: str
    expected_output: str


class TestCaseResponse(BaseModel):
    id: int
    problem_id: int
    input_data: str
    expected_output: str
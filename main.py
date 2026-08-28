from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {'message':'hello doll'}

problems = [
    {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "Easy"
    },
    {
        "id": 2,
        "title": "Binary Tree Maximum Path Sum",
        "difficulty": "Hard"
    }
]

class Problem(BaseModel):
    id: int
    title: str
    difficulty: str

class createProblem(BaseModel):
    title: str      
    difficulty: str

@app.get("/problems", response_model = list[Problem])    #FastAPI/Pydantic will turn the dictionaries into the declared response shape.
async def get_problems():
    return problems


@app.get("/problems/{problem_id}", response_model = Problem)
async def specific_prblm(problem_id:int):   #FastAPI will automatically return a validation error instead of your function receiving "abc" as a valid ID.
    for problem in problems:
        if(problem["id"] == problem_id):
            return problem

    raise HTTPException(
        status_code=404,
        detail = f"problem id {problem_id} not found!"
    )


# FastAPI uses Pydantic heavily for validating and structuring incoming data.

@app.post("/problems", response_model = Problem, status_code=status.HTTP_201_CREATED)                              #Now FastAPI knows: For a POST /problems, expect a JSON body matching Problem.
async def create_problem(problem:createProblem):
    new_problem = {
        "id":len(problems)+1,
        "title":problem.title,
        "difficulty":problem.difficulty
    }

    problems.append(new_problem)
    return new_problem
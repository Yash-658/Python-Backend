from fastapi import FastAPI, HTTPException
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

@app.get("/problems")
async def get_problems():
    newList = []
    for problem in problems:
        new_problem = Problem(
            title = problem["title"],
            difficulty = problem["difficulty"]
        )
        newList.append(new_problem)
    return newList


@app.get("/problems/{problem_id}")
async def specific_prblm(problem_id:int):   #FastAPI will automatically return a validation error instead of your function receiving "abc" as a valid ID.
    for problem in problems:
        if(problem["id"] == problem_id):
            prblm = Problem(
                title = problem["title"],
                difficulty= problem["difficulty"]
            )
            return prblm

    raise HTTPException(
        status_code=404,
        detail = f"problem id {problem_id} not found!"
    )
 


# FastAPI uses Pydantic heavily for validating and structuring incoming data.

class Problem(BaseModel):
    title: str
    difficulty: str

@app.post("/problems")                              #Now FastAPI knows: For a POST /problems, expect a JSON body matching Problem.
async def create_problem(problem:Problem):
    new_problem = {
        "id":len(problems)+1,
        "title":problem.title,
        "difficulty":problem.difficulty
    }

    problems.append(new_problem)
    return new_problem
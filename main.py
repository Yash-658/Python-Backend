from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel                      # FastAPI uses Pydantic heavily for validating and structuring incoming data.
from database import ProblemDB, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError           # IntegrityError is a SQLAlchemy exception that represents a database integrity constraint violation.

class Problem(BaseModel):     # data validation model (response model)
    id: int
    title: str
    difficulty: str

class ProblemCreate(BaseModel):     # data validation model (request model)
    title: str      
    difficulty: str


app = FastAPI()

@app.get("/")

async def root():
    return {'message':'hello doll'}


@app.get("/problems", response_model = list[Problem])    #FastAPI/Pydantic will turn the dictionaries into the declared response shape.

async def get_problems(db: Session = Depends(get_db)):
    problems = db.query(ProblemDB).all()

    return problems


@app.get("/problems/{problem_id}", response_model = Problem)

async def specific_prblm(problem_id:int, db: Session = Depends(get_db)):   #FastAPI will automatically return a validation error instead of your function receiving "abc" as a valid ID.
    this_problem = db.query(ProblemDB).filter(ProblemDB.id == problem_id).first()

    if this_problem:
        return this_problem

    raise HTTPException(
        status_code=404,
        detail = f"problem id {problem_id} not found!"
    )


@app.post("/problems", response_model = Problem, status_code=status.HTTP_201_CREATED)    #Now FastAPI knows: For a POST /problems, expect a JSON body matching Problem.

async def create_problem(problem:ProblemCreate, db: Session = Depends(get_db)):
    new_problem = ProblemDB(
        title = problem.title,
        difficulty = problem.difficulty
    )

    try:
        db.add(new_problem)
        db.commit()
        db.refresh(new_problem)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,                                        # 409 - The request conflicts with the current state of the resource.
            detail="An Integrity constraint has been violated~"
        )
    
    except Exception:
        db.rollback()
        raise
    
    return new_problem   # SQLAlchemy has populated the generated id on your new_problem ORM object.
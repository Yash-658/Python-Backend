from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError                     # IntegrityError is a SQLAlchemy exception that represents a database integrity constraint violation.

from sqlalchemy.orm import Session
from app.schemas.problems import Problem, ProblemCreate, ProblemUpdate

from app.database import get_db
from app.models.problemDB import ProblemDB

router = APIRouter(prefix="/problems", tags=["Problems"])     # tags=["Problems"] simply groups these endpoints under Problems in Swagger /docs.


@router.get("", response_model = list[Problem])    #FastAPI/Pydantic will turn the dictionaries into the declared response shape.

async def get_problems(db: Session = Depends(get_db)):
    problems = db.query(ProblemDB).all()

    return problems


@router.get("/{problem_id}", response_model = Problem)

async def specific_prblm(problem_id:int, db: Session = Depends(get_db)):   #FastAPI will automatically return a validation error instead of your function receiving "abc" as a valid ID.
    this_problem = db.query(ProblemDB).filter(ProblemDB.id == problem_id).first()

    if this_problem:
        return this_problem

    raise HTTPException(
        status_code=404,
        detail = f"problem id {problem_id} not found!"
    )
    
    
@router.post("", response_model = Problem, status_code=status.HTTP_201_CREATED)    #Now FastAPI knows: For a POST /problems, expect a JSON body matching Problem.

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


@router.patch("/{problem_id}", response_model = Problem)

async def update_problem(
    problem_id: int,
    problem: ProblemUpdate,
    db: Session = Depends(get_db)
):
    this_problem = (
        db.query(ProblemDB).filter(ProblemDB.id == problem_id).first()
    )
    
    if this_problem == None:
        raise HTTPException(
            status_code = 404,
            detail = f"Problem id {problem_id} not found!"
        )
        
    if problem.title is not None:
        this_problem.title = problem.title
    
    if problem.difficulty is not None:
        this_problem.difficulty = problem.difficulty
        
    try:
        db.commit()
        db.refresh(this_problem)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail = f"An Integrity constraint has been violated while updating this problem with id: {problem_id}"
        )
        
    except Exception:
        db.rollback()
        raise
    
    return this_problem


@router.delete("/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)   # 204 - The request succeeded, but there's no response body to return.

async def delete_problem(
    problem_id: int,
    db: Session = Depends(get_db)):
    
    this_problem = (db.query(ProblemDB).filter(ProblemDB.id == problem_id).first())
    
    if this_problem is None:
        raise HTTPException(
            status_code=404,
            detail=f"Problem with problem ID: {problem_id} not found!"
        )
    
    db.delete(this_problem)
    
    try:
        db.commit()
        
    except Exception:
        db.rollback()
        raise 
    
    return None
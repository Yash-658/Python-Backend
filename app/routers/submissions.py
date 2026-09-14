from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.dependencies import get_current_user
from app.models.submissionDB import SubmissionDB
from app.models.userDB import UserDB
from app.schemas.submissions import SubmissionCreate, SubmissionResponse

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"]
)

@router.post(
    "",
    response_model = SubmissionResponse,
    status_code = status.HTTP_201_CREATED
)

async def create_submission(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    new_submission = SubmissionDB(
        user_id = current_user.id,
        problem_id = submission.problem_id,
        code = submission.code,
        language = submission.language,
    )
    
    try:
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)

    except IntegrityError:                  # it will only happen when a problem_id we are trying to push with the submission doesn't really exist~
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )

    except Exception:
        db.rollback()
        raise
    
@router.get(
    "", 
    response_model=list[SubmissionResponse],
    status_code=status.HTTP_200_OK)

async def get_submissions(                                        # gets all submissions of the current user~
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(SubmissionDB).filter(SubmissionDB.user_id == current_user.id).all()         # implemeneted resource ownership, so they can only see submissions of themselves~
from sqlalchemy.orm import Session
from app.models.submissionDB import SubmissionDB

PENDING = "pending"
RUNNING = "running"
ACCEPTED = "accepted"
WRONG_ANSWER = "wrong_answer"
RUNTIME_ERROR = "runtime_error"
COMPILATION_ERROR = "compilation_error"
TIME_LIMIT_EXCEEDED = "time_limit_exceeded"


def judge_submission(
    submission: SubmissionDB,
    db: Session
):
    submission.status = RUNNING
    db.commit()
    
    problem = submission.problem

    for testcase in problem.test_cases:
        print(
            f"Running test case: "
            f"{testcase.input_data} -> {testcase.expected_output}"
        )
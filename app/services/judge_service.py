from sqlalchemy.orm import Session

from app.models.submissionDB import SubmissionDB


def judge_submission(
    submission: SubmissionDB,
    db: Session
):
    problem = submission.problem

    for testcase in problem.test_cases:
        print(
            f"Running test case: "
            f"{testcase.input_data} -> {testcase.expected_output}"
        )
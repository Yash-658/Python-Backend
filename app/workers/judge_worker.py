import logging

from rq import SimpleWorker
from rq.timeouts import TimerDeathPenalty

from app.database import SessionLocal
from app.models import SubmissionDB, ProblemDB
from app.services.judge_service import judge_submission
from app.queue import judge_queue


logger = logging.getLogger(__name__)


def judge_submission_job(submission_id: int) -> None:

    db = SessionLocal()

    try:
        # Fetch the submission from PostgreSQL.
        submission = (
            db.query(SubmissionDB)
            .filter(SubmissionDB.id == submission_id)
            .first()
        )

        if submission is None:
            logger.error("Submission %s not found", submission_id)
            return

        # Fetch its associated problem.
        problem = (
            db.query(ProblemDB)
            .filter(ProblemDB.id == submission.problem_id)
            .first()
        )

        if problem is None:
            submission.status = "judge_error"
            submission.error_message = "Problem not found."
            db.commit()
            return

        # Mark the submission as currently being judged.
        submission.status = "judging"
        submission.error_message = None                 # We must clear the previous error message so the final accepted submission doesn't incorrectly retain an old failure message.
        db.commit()

        # Execute the existing judging logic.
        verdict = judge_submission(
            submission.code,
            problem.test_cases
        )

        # Save the final results.
        submission.status = verdict.status
        submission.passed_test_cases = verdict.passed_test_cases
        submission.total_test_cases = verdict.total_test_cases
        submission.execution_time = verdict.execution_time
        submission.memory_used = verdict.memory_used

        db.commit()

    except Exception:
        db.rollback()
        logger.exception(
            "Judging failed for submission %s",
            submission_id
        )

        # Record an internal judging failure in PostgreSQL.
        try:
            submission = (
                db.query(SubmissionDB)
                .filter(SubmissionDB.id == submission_id)
                .first()
            )

            if submission is not None:
                submission.status = "judge_error"
                submission.error_message = (
                    "An internal error occurred while judging."
                )
                db.commit()

        except Exception:
            db.rollback()
            logger.exception("Could not update failed submission status")

        raise     # RQ needs the exception to know the job failed and should be retried.

    finally:
        db.close()


# Windows-compatible worker for local development. In linux we won't need this~
class WindowsSimpleWorker(SimpleWorker):
    death_penalty_class = TimerDeathPenalty


if __name__ == "__main__":              # This condition checks whether the Python file is being executed directly.
    worker = WindowsSimpleWorker(
        [judge_queue],
        connection=judge_queue.connection
    )

    worker.work()

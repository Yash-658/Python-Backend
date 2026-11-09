# Manual failed job management tool~

import argparse

from rq.job import Job

from app.queue import judge_queue
from app.database import SessionLocal
from app.models import SubmissionDB


failed_registry = judge_queue.failed_job_registry


def list_failed_jobs():
    job_ids = failed_registry.get_job_ids()

    if not job_ids:
        print("No failed judging jobs.")
        return

    for job_id in job_ids:
        job = Job.fetch(
            job_id,
            connection=judge_queue.connection
        )

        submission_id = job.args[0] if job.args else "Unknown"

        print("-" * 50)
        print(f"RQ Job ID: {job_id}")
        print(f"Submission ID: {submission_id}")
        print(f"Function: {job.func_name}")
        print("Exception details:")
        print(job.exc_info or "No traceback available.")

    print("-" * 50)


def requeue_failed_job(job_id: str):
    # Confirm that this job is actually in the failed registry.
    if job_id not in failed_registry.get_job_ids():
        raise ValueError("Job not found in the failed registry.")

    job = Job.fetch(
        job_id,
        connection=judge_queue.connection
    )

    # Only allow recovery of our judging jobs.
    expected_function = "app.workers.judge_worker.judge_submission_job"

    if job.func_name != expected_function:
        raise ValueError("This is not a submission judging job.")

    if not job.args:
        raise ValueError("The job does not contain a submission ID.")

    submission_id = job.args[0]

    # Reset the database submission before requeueing.
    db = SessionLocal()

    try:
        submission = (
            db.query(SubmissionDB)
            .filter(SubmissionDB.id == submission_id)
            .first()
        )

        if submission is None:
            raise ValueError("Associated submission does not exist.")

        submission.status = "pending"
        submission.error_message = None
        submission.passed_test_cases = 0
        submission.total_test_cases = 0
        submission.execution_time = None
        submission.memory_used = None

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

    try:
        # Move the failed job back into its original queue.
        failed_registry.requeue(job_id)

    except Exception:
        # Restore the failure status if requeueing itself fails.
        db = SessionLocal()

        try:
            submission = (
                db.query(SubmissionDB)
                .filter(SubmissionDB.id == submission_id)
                .first()
            )

            if submission is not None:
                submission.status = "judge_error"
                submission.error_message = (
                    "Manual retry could not be queued."
                )
                db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        raise

    print(f"Submission {submission_id} successfully requeued.")


def main():
    parser = argparse.ArgumentParser(
        description="Manage failed coding-platform judging jobs."
    )

    parser.add_argument(
        "action",
        choices=["list", "requeue"],
        help="List failed jobs or requeue one."
    )

    parser.add_argument(
        "job_id",
        nargs="?",
        help="RQ job ID required for requeue."
    )

    args = parser.parse_args()

    if args.action == "list":
        if args.job_id:
            parser.error("Do not provide a job ID when listing.")

        list_failed_jobs()

    elif args.action == "requeue":
        if not args.job_id:
            parser.error("A job ID is required for requeue.")

        requeue_failed_job(args.job_id)


if __name__ == "__main__":
    main()

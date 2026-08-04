from datetime import datetime, timedelta

from celery_worker import celery_app
from db.db import db
from model.model import ExportJobModel, ExportStatus


def is_celery_worker_available(timeout=1.0):
    try:
        inspector = celery_app.control.inspect(timeout=timeout)
        ping_result = inspector.ping()
        return bool(ping_result)
    except Exception as exc:
        print(f"Celery worker check failed: {exc}")
        return False


def fail_stale_export_jobs(user_id=None, max_age_seconds=120):
    """Mark old pending/processing export jobs as failed (worker was likely down)."""
    cutoff = datetime.utcnow() - timedelta(seconds=max_age_seconds)

    query = ExportJobModel.query.filter(
        ExportJobModel.status.in_([ExportStatus.PENDING, ExportStatus.PROCESSING]),
        ExportJobModel.created_at < cutoff,
    )

    if user_id is not None:
        query = query.filter_by(user_id=user_id)

    stale_jobs = query.all()
    if not stale_jobs:
        return 0

    for job in stale_jobs:
        job.status = ExportStatus.FAILED

    db.session.commit()
    return len(stale_jobs)

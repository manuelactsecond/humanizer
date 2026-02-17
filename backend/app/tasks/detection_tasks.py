"""Celery tasks for async detection (used in Phase 3 for large documents)."""

from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, name="detect_document")
def detect_document(self, document_id: str, text: str, language: str):
    """Async detection for large documents. Placeholder for Phase 3."""
    pass

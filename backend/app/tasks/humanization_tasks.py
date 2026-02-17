"""Celery tasks for async humanization (used in Phase 3 for large documents)."""

from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, name="humanize_document")
def humanize_document(self, document_id: str, text: str, language: str, intensity: str):
    """Async humanization for large documents. Placeholder for Phase 3."""
    pass

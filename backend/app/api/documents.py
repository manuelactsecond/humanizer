import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/", response_model=DocumentResponse, status_code=201)
async def create_document(
    doc: DocumentCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a document record for tracking."""
    document = Document(
        original_text=doc.text,
        language=doc.language,
        word_count=len(doc.text.split()),
        status="pending",
    )
    db.add(document)
    await db.flush()
    await db.refresh(document)
    return document


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a document by ID."""
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

from typing import List, Optional
from sqlalchemy.orm import Session
from backend.database.models import Document, DocumentChunk


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_document(self, document_id: str) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_chunks_by_standard(self, standard_id: str) -> List[DocumentChunk]:
        return (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.standard_id == standard_id)
            .order_by(DocumentChunk.chunk_index)
            .all()
        )

    def get_chunks_by_clause(self, is_number: str, clause: str) -> List[DocumentChunk]:
        return (
            self.db.query(DocumentChunk)
            .filter(
                DocumentChunk.is_number.ilike(f"%{is_number}%"),
                DocumentChunk.clause.ilike(f"%{clause}%"),
            )
            .all()
        )

    def create_document(self, document: Document) -> Document:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def create_chunk(self, chunk: DocumentChunk) -> DocumentChunk:
        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk

    def bulk_create_chunks(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        self.db.add_all(chunks)
        self.db.commit()
        return chunks

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, desc
from backend.database.models import Standard, Amendment, DocumentChunk


class StandardsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, standard_id: str) -> Optional[Standard]:
        return (
            self.db.query(Standard)
            .options(joinedload(Standard.amendments), joinedload(Standard.documents))
            .filter(Standard.id == standard_id)
            .first()
        )

    def get_by_is_number(self, is_number: str) -> Optional[Standard]:
        normalized = is_number.strip()
        standard = (
            self.db.query(Standard)
            .options(joinedload(Standard.amendments))
            .filter(func.lower(Standard.is_number) == normalized.lower())
            .first()
        )
        if not standard and not ":" in normalized:
            standard = (
                self.db.query(Standard)
                .options(joinedload(Standard.amendments))
                .filter(Standard.is_number.ilike(f"{normalized}:%"))
                .first()
            )
        if not standard:
            standard = (
                self.db.query(Standard)
                .options(joinedload(Standard.amendments))
                .filter(Standard.is_number.ilike(f"%{normalized}%"))
                .first()
            )
        return standard

    def search(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        industry: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Standard]:
        stmt = self.db.query(Standard).options(joinedload(Standard.amendments))
        
        if category:
            stmt = stmt.filter(Standard.category.ilike(f"%{category}%"))
        if industry:
            stmt = stmt.filter(Standard.industry.ilike(f"%{industry}%"))
        if status:
            stmt = stmt.filter(Standard.status.ilike(status))

        all_candidates = stmt.all()

        if not query:
            return all_candidates[offset:offset + limit]

        clean_q = query.lower().strip()
        tokens = [t for t in clean_q.split() if len(t) > 2 and t not in ["and", "for", "the", "with", "type", "what", "which", "cover"]]

        # Python-level multi-token scoring
        scored_candidates = []
        for std in all_candidates:
            haystack = f"{std.is_number} {std.title} {std.keywords or ''} {std.scope or ''}".lower()
            score = 0.0

            # Exact phrase match in title or keywords
            if clean_q in haystack:
                score += 10.0

            # Individual token matches
            matched_tokens = 0
            for t in tokens:
                if t in haystack:
                    matched_tokens += 1
                    score += 2.0

            # Boost if all search tokens are matched
            if tokens and matched_tokens == len(tokens):
                score += 5.0

            if score > 0:
                scored_candidates.append((score, std))

        # Sort descending by score
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return [std for score, std in scored_candidates[offset:offset + limit]]

    def get_all(self, limit: int = 100) -> List[Standard]:
        return self.db.query(Standard).options(joinedload(Standard.amendments)).limit(limit).all()

    def create(self, standard: Standard) -> Standard:
        self.db.add(standard)
        self.db.commit()
        self.db.refresh(standard)
        return standard

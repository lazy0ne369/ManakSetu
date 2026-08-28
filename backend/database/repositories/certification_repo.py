from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.database.models import CertificationScheme


class CertificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_scheme_id(self, scheme_id: str) -> Optional[CertificationScheme]:
        return (
            self.db.query(CertificationScheme)
            .filter(CertificationScheme.scheme_id.ilike(scheme_id.strip()))
            .first()
        )

    def get_by_product_or_keyword(self, keyword: str) -> List[CertificationScheme]:
        pattern = f"%{keyword.strip()}%"
        return (
            self.db.query(CertificationScheme)
            .filter(
                or_(
                    CertificationScheme.applicable_products.ilike(pattern),
                    CertificationScheme.scheme_name.ilike(pattern),
                    CertificationScheme.description.ilike(pattern),
                )
            )
            .all()
        )

    def get_all(self) -> List[CertificationScheme]:
        return self.db.query(CertificationScheme).all()

    def create(self, scheme: CertificationScheme) -> CertificationScheme:
        self.db.add(scheme)
        self.db.commit()
        self.db.refresh(scheme)
        return scheme

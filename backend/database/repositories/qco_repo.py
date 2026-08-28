from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from backend.database.models import QCO


class QCORepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, qco_id: str) -> Optional[QCO]:
        return self.db.query(QCO).filter(QCO.id == qco_id).first()

    def get_by_is_number(self, is_number: str) -> List[QCO]:
        clean_is = is_number.strip()
        # Search exact or base number (e.g. "IS 2347" inside "IS 2347:2017")
        base_is = clean_is.split(":")[0].strip() if ":" in clean_is else clean_is
        return (
            self.db.query(QCO)
            .filter(
                or_(
                    func.lower(QCO.is_number) == clean_is.lower(),
                    QCO.is_number.ilike(f"%{base_is}%"),
                )
            )
            .all()
        )

    def get_by_product(self, product_name: str) -> List[QCO]:
        clean_prod = product_name.strip()
        return (
            self.db.query(QCO)
            .filter(
                or_(
                    QCO.product_name.ilike(f"%{clean_prod}%"),
                    QCO.title.ilike(f"%{clean_prod}%"),
                )
            )
            .all()
        )

    def search(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[QCO]:
        stmt = self.db.query(QCO)
        if query:
            pattern = f"%{query}%"
            stmt = stmt.filter(
                or_(
                    QCO.qco_number.ilike(pattern),
                    QCO.title.ilike(pattern),
                    QCO.product_name.ilike(pattern),
                    QCO.is_number.ilike(pattern),
                    QCO.ministry.ilike(pattern),
                )
            )
        if status:
            stmt = stmt.filter(QCO.status.ilike(status))
        return stmt.limit(limit).all()

    def get_all(self, limit: int = 100) -> List[QCO]:
        return self.db.query(QCO).limit(limit).all()

    def create(self, qco: QCO) -> QCO:
        self.db.add(qco)
        self.db.commit()
        self.db.refresh(qco)
        return qco

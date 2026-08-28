# Seed script to populate knowledge base into Database
import logging
from sqlalchemy.orm import Session
from backend.database.session import SessionLocal, init_db
from backend.database.models import (
    Standard,
    Amendment,
    QCO,
    CertificationScheme,
    Document,
    DocumentChunk,
    Source,
)
from backend.knowledge.standards import SEED_STANDARDS
from backend.knowledge.qco import SEED_QCOS
from backend.knowledge.certification import SEED_SCHEMES
from backend.knowledge.amendments import SEED_AMENDMENTS

logger = logging.getLogger(__name__)


def seed_database(db: Session = None) -> None:
    close_session = False
    if db is None:
        init_db()
        db = SessionLocal()
        close_session = True

    try:
        logger.info("Seeding Standards & Clauses...")
        standards_map = {}
        for s_data in SEED_STANDARDS:
            clauses = s_data.get("clauses", [])
            existing = db.query(Standard).filter(Standard.is_number == s_data["is_number"]).first()
            if not existing:
                standard = Standard(
                    is_number=s_data["is_number"],
                    title=s_data["title"],
                    year=s_data["year"],
                    status=s_data["status"],
                    scope=s_data["scope"],
                    category=s_data["category"],
                    industry=s_data["industry"],
                    committee=s_data["committee"],
                    keywords=s_data["keywords"],
                    publication_date=s_data["publication_date"],
                    effective_date=s_data["effective_date"],
                    source_url=s_data["source_url"],
                    is_demo=s_data["is_demo"],
                )
                db.add(standard)
                db.flush()
                standards_map[s_data["is_number"]] = standard

                # Create Document entry
                doc = Document(
                    standard_id=standard.id,
                    title=f"Standard Specification — {s_data['is_number']}",
                    document_type="standard",
                    filename=f"{s_data['is_number'].replace(':', '_').replace(' ', '_')}.pdf",
                    total_pages=max([c.get("page", 1) for c in clauses] or [1]),
                    source_url=s_data["source_url"],
                    is_demo=s_data["is_demo"],
                )
                db.add(doc)
                db.flush()

                # Add Chunks
                for idx, c in enumerate(clauses):
                    chunk = DocumentChunk(
                        document_id=doc.id,
                        standard_id=standard.id,
                        is_number=s_data["is_number"],
                        section=c.get("section", ""),
                        clause=c.get("clause", ""),
                        page=c.get("page", 1),
                        chunk_index=idx,
                        content=f"[{s_data['is_number']} Clause {c.get('clause')} - {c.get('title')}]\n{c.get('content')}",
                        token_count=len(c.get("content", "").split()),
                        metadata_json={
                            "standard": s_data["is_number"],
                            "section": c.get("section"),
                            "clause": c.get("clause"),
                            "title": c.get("title"),
                            "page": c.get("page"),
                            "category": s_data["category"],
                            "industry": s_data["industry"],
                            "document_status": s_data["status"],
                            "source": "BIS Official",
                        },
                        is_demo=s_data["is_demo"],
                    )
                    db.add(chunk)
            else:
                standards_map[s_data["is_number"]] = existing

        logger.info("Seeding QCOs...")
        for q_data in SEED_QCOS:
            existing = db.query(QCO).filter(QCO.qco_number == q_data["qco_number"]).first()
            if not existing:
                qco = QCO(
                    qco_number=q_data["qco_number"],
                    title=q_data["title"],
                    product_name=q_data["product_name"],
                    is_number=q_data["is_number"],
                    ministry=q_data["ministry"],
                    notification_date=q_data["notification_date"],
                    enforcement_date=q_data["enforcement_date"],
                    status=q_data["status"],
                    source_url=q_data["source_url"],
                    notes=q_data["notes"],
                    is_demo=q_data["is_demo"],
                )
                db.add(qco)

        logger.info("Seeding Certification Schemes...")
        for sch_data in SEED_SCHEMES:
            existing = db.query(CertificationScheme).filter(CertificationScheme.scheme_id == sch_data["scheme_id"]).first()
            if not existing:
                scheme = CertificationScheme(
                    scheme_id=sch_data["scheme_id"],
                    scheme_name=sch_data["scheme_name"],
                    description=sch_data["description"],
                    applicable_products=sch_data["applicable_products"],
                    requirements=sch_data["requirements"],
                    testing_info=sch_data["testing_info"],
                    fee_structure=sch_data["fee_structure"],
                    source_url=sch_data["source_url"],
                    status=sch_data["status"],
                    is_demo=sch_data["is_demo"],
                )
                db.add(scheme)

        logger.info("Seeding Amendments...")
        for a_data in SEED_AMENDMENTS:
            std = standards_map.get(a_data["is_number"]) or db.query(Standard).filter(Standard.is_number == a_data["is_number"]).first()
            if std:
                existing = db.query(Amendment).filter(
                    Amendment.standard_id == std.id,
                    Amendment.amendment_number == a_data["amendment_number"]
                ).first()
                if not existing:
                    amendment = Amendment(
                        standard_id=std.id,
                        amendment_number=a_data["amendment_number"],
                        title=a_data["title"],
                        publication_date=a_data["publication_date"],
                        effective_date=a_data["effective_date"],
                        notes=a_data["notes"],
                        source_url=a_data["source_url"],
                        is_demo=a_data["is_demo"],
                    )
                    db.add(amendment)

        logger.info("Seeding Official Sources...")
        sources = [
            {
                "name": "Bureau of Indian Standards — e-BIS Portal",
                "url": "https://www.services.bis.gov.in/",
                "organization": "Bureau of Indian Standards",
                "source_type": "Official Portal",
                "description": "Primary authority portal for Indian Standards, Know Your Standard, and License search.",
                "last_verified": "2026-08-01",
            },
            {
                "name": "DPIIT Quality Control Orders Portal",
                "url": "https://dpiit.gov.in/quality-control-orders",
                "organization": "Department for Promotion of Industry and Internal Trade",
                "source_type": "Gazette & QCO Portal",
                "description": "Official gazette notifications for mandatory standard enforcement under BIS Act, 2016.",
                "last_verified": "2026-08-01",
            },
            {
                "name": "Compulsory Registration Scheme (CRS) Portal",
                "url": "https://www.crsbis.in/BIS/",
                "organization": "MeitY / BIS",
                "source_type": "Registration Portal",
                "description": "Portal for electronic & IT goods compliance under Scheme-II.",
                "last_verified": "2026-08-01",
            }
        ]
        for src in sources:
            existing = db.query(Source).filter(Source.url == src["url"]).first()
            if not existing:
                s_obj = Source(
                    name=src["name"],
                    url=src["url"],
                    organization=src["organization"],
                    source_type=src["source_type"],
                    description=src["description"],
                    last_verified=src["last_verified"],
                    is_demo=False,
                )
                db.add(s_obj)

        db.commit()
        logger.info("Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        if close_session:
            db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_database()

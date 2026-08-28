from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.database.models import Standard, QCO, CertificationScheme, Amendment
from backend.database.repositories.standards_repo import StandardsRepository
from backend.database.repositories.qco_repo import QCORepository
from backend.database.repositories.certification_repo import CertificationRepository
from backend.rag.schemas import (
    ParsedQuery,
    ApplicableStandardItem,
    QCOItem,
)


class ComplianceResolver:
    def __init__(self, db: Session):
        self.db = db
        self.standards_repo = StandardsRepository(db)
        self.qco_repo = QCORepository(db)
        self.cert_repo = CertificationRepository(db)

    def resolve(
        self,
        parsed_query: ParsedQuery,
        retrieved_is_numbers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        applicable_standards: List[ApplicableStandardItem] = []
        matching_qcos: List[QCOItem] = []
        schemes_found: List[Dict[str, Any]] = []
        amendments_found: List[Dict[str, Any]] = []

        candidate_standards = []

        # 1. Exact IS number lookup if provided in query
        if parsed_query.is_number:
            std = self.standards_repo.get_by_is_number(parsed_query.is_number)
            if std:
                candidate_standards.append(std)

        # 2. Product name lookup
        if parsed_query.product:
            std_by_prod = self.standards_repo.search(query=parsed_query.product, limit=3)
            for s in std_by_prod:
                if s not in candidate_standards:
                    candidate_standards.append(s)

        # 3. If no explicit standard/product found, fallback to retrieved chunks
        if not candidate_standards and retrieved_is_numbers:
            for is_num in retrieved_is_numbers[:3]:
                std = self.standards_repo.get_by_is_number(is_num)
                if std and std not in candidate_standards:
                    candidate_standards.append(std)

        # 4. Resolve QCOs and Certification status for each candidate standard
        for std in candidate_standards:
            # Check QCOs
            qcos = self.qco_repo.get_by_is_number(std.is_number)
            is_mandatory = False
            qco_num = None

            for q in qcos:
                matching_qcos.append(
                    QCOItem(
                        qco_number=q.qco_number,
                        title=q.title,
                        product_name=q.product_name,
                        is_number=q.is_number,
                        ministry=q.ministry,
                        status=q.status,
                        enforcement_date=q.enforcement_date,
                        source_url=q.source_url,
                    )
                )
                if q.status.lower() == "mandatory":
                    is_mandatory = True
                    qco_num = q.qco_number

            # Determine scheme
            scheme_name = "Scheme-I (ISI Mark)"
            if "CRS" in (std.keywords or "") or "Electronics" in (std.industry or ""):
                scheme_name = "Scheme-II (CRS)"

            applicable_standards.append(
                ApplicableStandardItem(
                    is_number=std.is_number,
                    title=std.title,
                    year=std.year,
                    status=std.status,
                    mandatory=is_mandatory,
                    qco_number=qco_num,
                    certification_scheme=scheme_name,
                    applicability_reason=f"Applies to {std.industry or 'product'} under scope: {std.scope[:150]}..." if std.scope else "Direct standard match",
                    source_url=std.source_url,
                )
            )

            # Amendments
            for amd in std.amendments:
                amendments_found.append({
                    "is_number": std.is_number,
                    "amendment_number": amd.amendment_number,
                    "title": amd.title,
                    "effective_date": amd.effective_date,
                    "notes": amd.notes,
                })

        # Fetch relevant schemes
        all_schemes = self.cert_repo.get_all()
        for sch in all_schemes:
            schemes_found.append({
                "scheme_id": sch.scheme_id,
                "scheme_name": sch.scheme_name,
                "description": sch.description,
                "requirements": sch.requirements,
                "testing_info": sch.testing_info,
            })

        certification_status = "Mandatory" if any(s.mandatory for s in applicable_standards) else "Voluntary" if applicable_standards else "Pending Clarification"

        return {
            "applicable_standards": applicable_standards,
            "qcos": matching_qcos,
            "certification_schemes": schemes_found,
            "amendments": amendments_found,
            "certification_status": certification_status,
        }

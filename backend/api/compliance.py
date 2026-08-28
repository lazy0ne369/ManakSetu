from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.rag.compliance import ComplianceResolver
from backend.rag.schemas import ParsedQuery

router = APIRouter(prefix="/api/compliance", tags=["Compliance & QCO"])


@router.get(
    "/{product}",
    summary="Get regulatory compliance status, QCOs, and certification route for a product",
)
def get_compliance_for_product(
    product: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    resolver = ComplianceResolver(db)
    parsed = ParsedQuery(
        original_query=f"Compliance for {product}",
        product=product,
        user_role="industry",
    )
    result = resolver.resolve(parsed_query=parsed)

    if not result["applicable_standards"]:
        return {
            "product": product,
            "status": "No specific Indian Standard found in local database",
            "is_mandatory": False,
            "applicable_standards": [],
            "qcos": [],
            "certification_schemes": [],
        }

    return {
        "product": product,
        "certification_status": result["certification_status"],
        "applicable_standards": [s.model_dump() for s in result["applicable_standards"]],
        "qcos": [q.model_dump() for q in result["qcos"]],
        "certification_schemes": result["certification_schemes"],
        "amendments": result["amendments"],
    }

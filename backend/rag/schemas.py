from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    CONSUMER = "consumer"
    INDUSTRY = "industry"
    AUDITOR = "auditor"


class QueryIntent(str, Enum):
    STANDARD_LOOKUP = "STANDARD_LOOKUP"
    CERTIFICATION = "CERTIFICATION"
    QCO = "QCO"
    COMPLIANCE = "COMPLIANCE"
    AMENDMENT = "AMENDMENT"
    STANDARD_COMPARISON = "STANDARD_COMPARISON"
    LABORATORY = "LABORATORY"
    GENERAL_BIS_SERVICE = "GENERAL_BIS_SERVICE"


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ParsedQuery(BaseModel):
    original_query: str
    product: Optional[str] = None
    material: Optional[str] = None
    intended_use: Optional[str] = None
    industry: Optional[str] = None
    user_role: UserRole = UserRole.CONSUMER
    intent: QueryIntent = QueryIntent.STANDARD_LOOKUP
    is_number: Optional[str] = None
    constraints: List[str] = Field(default_factory=list)
    needs_clarification: bool = False
    clarification_question: Optional[str] = None


class ApplicableStandardItem(BaseModel):
    is_number: str
    title: str
    year: Optional[int] = None
    status: str = "Active"
    mandatory: bool = False
    qco_number: Optional[str] = None
    certification_scheme: Optional[str] = None
    applicability_reason: Optional[str] = None
    source_url: Optional[str] = None


class QCOItem(BaseModel):
    qco_number: str
    title: str
    product_name: str
    is_number: str
    ministry: Optional[str] = None
    status: str = "Mandatory"
    enforcement_date: Optional[str] = None
    source_url: Optional[str] = None


class CitationItem(BaseModel):
    standard: str
    clause: Optional[str] = None
    section: Optional[str] = None
    page: Optional[int] = None
    source_url: Optional[str] = None
    excerpt: Optional[str] = None


class EvidenceExcerpt(BaseModel):
    is_number: str
    section: Optional[str] = None
    clause: Optional[str] = None
    page: Optional[int] = None
    content: str
    score: float = 0.0
    source: str = "BIS Official"


class EvidencePack(BaseModel):
    standards: List[ApplicableStandardItem] = Field(default_factory=list)
    qcos: List[QCOItem] = Field(default_factory=list)
    certification_schemes: List[Dict[str, Any]] = Field(default_factory=list)
    amendments: List[Dict[str, Any]] = Field(default_factory=list)
    document_excerpts: List[EvidenceExcerpt] = Field(default_factory=list)
    sources: List[Dict[str, Any]] = Field(default_factory=list)


class StructuredResponse(BaseModel):
    answer: str
    applicable_standards: List[ApplicableStandardItem] = Field(default_factory=list)
    applicability_reason: Optional[str] = None
    certification_status: str = "Mandatory"  # "Mandatory", "Voluntary", "Pending Clarification", "Not Applicable"
    certification_scheme: Optional[str] = "Scheme-I (ISI Mark)"
    qcos: List[QCOItem] = Field(default_factory=list)
    key_requirements: List[str] = Field(default_factory=list)
    compliance_steps: List[str] = Field(default_factory=list)
    sources: List[CitationItem] = Field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.HIGH
    needs_clarification: bool = False
    clarification_question: Optional[str] = None

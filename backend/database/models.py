import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="consumer")  # "consumer", "industry", "auditor", "admin"
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(255), default="New Conversation")
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    user = relationship("User", back_populates="sessions")
    messages = relationship("QueryLog", back_populates="session", cascade="all, delete-orphan")


class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=True, index=True)
    user_query = Column(Text, nullable=False)
    role_type = Column(String(50), default="consumer")  # "consumer", "industry"
    intent = Column(String(100), nullable=True)
    parsed_entities = Column(JSON, nullable=True)
    raw_response = Column(JSON, nullable=True)
    confidence = Column(String(20), default="MEDIUM")  # "HIGH", "MEDIUM", "LOW"
    needs_clarification = Column(Boolean, default=False)
    clarification_question = Column(Text, nullable=True)
    citations = Column(JSON, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    session = relationship("Session", back_populates="messages")
    feedbacks = relationship("Feedback", back_populates="query_log", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_query_logs_intent", "intent"),
        Index("ix_query_logs_created_at", "created_at"),
    )


class Standard(Base):
    __tablename__ = "standards"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    is_number = Column(String(100), unique=True, index=True, nullable=False)  # e.g., "IS 2347:2017"
    title = Column(String(500), nullable=False, index=True)
    year = Column(Integer, nullable=True)
    status = Column(String(50), default="Active")  # "Active", "Superseded", "Withdrawn", "Under Revision"
    scope = Column(Text, nullable=True)
    category = Column(String(200), nullable=True, index=True)  # e.g. "Mechanical Engineering"
    industry = Column(String(200), nullable=True, index=True)  # e.g. "Cookware & Domestic Appliances"
    committee = Column(String(200), nullable=True)  # e.g. "MED 33"
    keywords = Column(Text, nullable=True)  # Comma-separated or search text
    publication_date = Column(String(50), nullable=True)
    effective_date = Column(String(50), nullable=True)
    superseded_standard = Column(String(100), nullable=True)
    source_url = Column(String(1000), nullable=True)
    document_url = Column(String(1000), nullable=True)
    is_demo = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    amendments = relationship("Amendment", back_populates="standard", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="standard", cascade="all, delete-orphan")
    chunks = relationship("DocumentChunk", back_populates="standard", cascade="all, delete-orphan")


class Amendment(Base):
    __tablename__ = "amendments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    standard_id = Column(String(36), ForeignKey("standards.id", ondelete="CASCADE"), nullable=False, index=True)
    amendment_number = Column(String(50), nullable=False)  # e.g. "Amendment 1", "Amendment 2"
    title = Column(String(500), nullable=True)
    publication_date = Column(String(50), nullable=True)
    effective_date = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    source_url = Column(String(1000), nullable=True)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    standard = relationship("Standard", back_populates="amendments")


class QCO(Base):
    __tablename__ = "qcos"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    qco_number = Column(String(100), unique=True, index=True, nullable=False)  # e.g. "S.O. 3968(E)"
    title = Column(String(500), nullable=False)
    product_name = Column(String(500), nullable=False, index=True)  # e.g. "Domestic Pressure Cooker"
    is_number = Column(String(100), nullable=False, index=True)  # e.g. "IS 2347:2017"
    ministry = Column(String(300), nullable=True)  # e.g. "Ministry of Commerce and Industry (DPIIT)"
    notification_date = Column(String(50), nullable=True)
    enforcement_date = Column(String(50), nullable=True)
    status = Column(String(50), default="Mandatory")  # "Mandatory", "Pending Enforcement", "Exempted"
    source_url = Column(String(1000), nullable=True)
    notes = Column(Text, nullable=True)
    is_demo = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    __table_args__ = (
        Index("ix_qcos_is_number_status", "is_number", "status"),
    )


class CertificationScheme(Base):
    __tablename__ = "certification_schemes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    scheme_id = Column(String(50), unique=True, index=True, nullable=False)  # e.g. "Scheme-I", "Scheme-II (CRS)"
    scheme_name = Column(String(255), nullable=False)  # e.g. "Product Certification Scheme (ISI Mark)"
    description = Column(Text, nullable=True)
    applicable_products = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    testing_info = Column(Text, nullable=True)
    fee_structure = Column(Text, nullable=True)
    source_url = Column(String(1000), nullable=True)
    status = Column(String(50), default="Active")
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    standard_id = Column(String(36), ForeignKey("standards.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(500), nullable=False)
    document_type = Column(String(50), default="standard")  # "standard", "qco", "guideline", "manual"
    filename = Column(String(255), nullable=True)
    file_path = Column(String(1000), nullable=True)
    file_size = Column(Integer, nullable=True)
    total_pages = Column(Integer, nullable=True)
    checksum = Column(String(64), nullable=True)
    source_url = Column(String(1000), nullable=True)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    standard = relationship("Standard", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=True, index=True)
    standard_id = Column(String(36), ForeignKey("standards.id", ondelete="CASCADE"), nullable=True, index=True)
    is_number = Column(String(100), index=True, nullable=True)
    section = Column(String(100), nullable=True)
    clause = Column(String(100), nullable=True, index=True)
    page = Column(Integer, nullable=True)
    chunk_index = Column(Integer, default=0)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=True)
    qdrant_point_id = Column(String(36), nullable=True, index=True)
    metadata_json = Column(JSON, nullable=True)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    document = relationship("Document", back_populates="chunks")
    standard = relationship("Standard", back_populates="chunks")

    __table_args__ = (
        Index("ix_chunks_clause_standard", "standard_id", "clause"),
    )


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    url = Column(String(1000), nullable=False)
    organization = Column(String(255), default="Bureau of Indian Standards (BIS)")
    source_type = Column(String(100), default="Official Portal")  # "Official Portal", "Gazette", "e-BIS"
    description = Column(Text, nullable=True)
    last_verified = Column(String(50), nullable=True)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    query_log_id = Column(String(36), ForeignKey("query_logs.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)  # 1 to 5 or 1 (up) / -1 (down)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    query_log = relationship("QueryLog", back_populates="feedbacks")

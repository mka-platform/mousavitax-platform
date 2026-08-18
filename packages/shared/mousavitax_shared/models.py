"""Shared data models for MousaviTax Platform (Pydantic).

Migrated from MKA-Core and extended per ADR-002 (Knowledge Data Model):
  - Temporal Validity (effective_from / effective_to)
  - official_ref for Iranian tax sources
  - SourceDocument entity
  - Tax-oriented SourceType values
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    """Origin or document category."""

    # Generic / ingestion
    GOOGLE_DRIVE = "google_drive"
    UPLOAD = "upload"
    MARKDOWN = "markdown"
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    PPTX = "pptx"
    HTML = "html"
    CSV = "csv"
    OCR = "ocr"
    MANUAL = "manual"

    # Iranian tax official categories (ADR-002)
    LAW = "law"
    CIRCULAR = "circular"
    RULING = "ruling"
    DIRECTIVE = "directive"
    REGULATION = "regulation"
    INSTRUCTION = "instruction"


class SourceDocument(BaseModel):
    """Canonical source document (law, circular, ruling, ...)."""

    source_id: str
    source_type: SourceType
    title: str
    official_ref: Optional[str] = None  # e.g. section number, circular no.
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    supersedes: Optional[str] = None  # source_id of previous version
    superseded_by: Optional[str] = None
    url: Optional[str] = None
    storage_path: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Citation(BaseModel):
    """Provenance for a retrieved chunk — mandatory for tax claims."""

    source_id: str
    source_type: SourceType
    title: str
    chunk_id: str
    score: float = Field(..., ge=0.0, le=1.0)
    page: Optional[int] = None
    section: Optional[str] = None
    url: Optional[str] = None
    official_ref: Optional[str] = None
    effective_from: Optional[date] = None


class RetrievedChunk(BaseModel):
    content: str
    citation: Citation
    metadata: dict[str, Any] = Field(default_factory=dict)


class RAGRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=20)
    filters: Optional[dict[str, Any]] = None
    # Optional as-of date for temporal filtering (ADR-002)
    as_of: Optional[date] = None


class RAGResponse(BaseModel):
    answer: str
    citations: list[Citation]
    model: str
    latency_ms: Optional[int] = None
    request_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# --- Knowledge / Vector Query models ---


class DocumentChunk(BaseModel):
    """A chunk ready for embedding and storage."""

    chunk_id: str
    source_id: str
    source_type: SourceType
    title: str
    text: str
    page: Optional[int] = None
    section: Optional[str] = None
    url: Optional[str] = None
    official_ref: Optional[str] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class IndexRequest(BaseModel):
    chunks: list[DocumentChunk]
    collection: str = "iran_tax_official"


class IndexResponse(BaseModel):
    indexed: int
    collection: str
    errors: list[str] = Field(default_factory=list)


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=20)
    filters: Optional[dict[str, Any]] = None
    collection: str = "iran_tax_official"
    as_of: Optional[date] = None  # temporal validity filter


class QueryHit(BaseModel):
    chunk_id: str
    text: str
    score: float
    citation: Citation


class QueryResponse(BaseModel):
    hits: list[QueryHit]
    query: str
    latency_ms: Optional[int] = None

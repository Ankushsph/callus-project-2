"""Pydantic schemas for API request/response models."""

from typing import List, Dict
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request model for essay analysis."""
    essay: str = Field(..., min_length=10, description="Essay text to analyze")


class SentenceResult(BaseModel):
    """Result for a single sentence."""
    text: str
    start_char: int
    end_char: int
    score: float = Field(..., ge=0, le=100, description="AI likelihood score (0-100)")
    signals: Dict[str, float] = Field(default_factory=dict, description="Individual signal scores")
    evidence: List[str] = Field(default_factory=list, description="Human-readable evidence")


class AnalyzeResponse(BaseModel):
    """Response model for essay analysis."""
    essay: str
    overall_score: float = Field(..., ge=0, le=100)
    verdict: str = Field(..., description="HUMAN, SUSPICIOUS, or AI_LIKELY")
    sentences: List[SentenceResult]
    summary: Dict[str, float] = Field(default_factory=dict, description="Summary statistics")

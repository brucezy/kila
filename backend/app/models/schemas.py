from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
from app.config import settings


class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000, description="The prompt text")
    project_name: str = Field(..., min_length=1, max_length=100, description="Project identifier")
    user_id: str = Field(..., min_length=1, max_length=100, description="User identifier")
    idempotency_key: str = Field(..., min_length=1, max_length=100, description="Unique key to prevent duplicates")
    company_id: str = Field(..., min_length=1, max_length=100, description="company identifier")


class PromptResponse(BaseModel):
    id: int
    prompt: str
    project_name: str
    user_id: str
    idempotency_key: str
    created_at: datetime
    is_duplicate: bool = False
    company_id: str
    is_active: bool


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str = settings.environment

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class BaseRequest(BaseModel):
    """Base class for all request models."""
    timestamp: datetime = Field(default_factory=datetime.now)
    
class BaseResponse(BaseModel):
    """Base class for all response models."""
    success: bool = True
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
class ErrorResponse(BaseResponse):
    """Standard error response model."""
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None 
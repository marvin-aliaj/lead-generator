from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class CheckinRequest(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    restaurant_id: str


class CheckinResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: Optional[str]
    restaurant_id: str
    created_at: str


class FeedbackRequest(BaseModel):
    customer_id: str
    rating: int
    improvement_areas: List[str]
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: str
    customer_id: str
    restaurant_id: str
    rating: int
    improvement_areas: List[str]
    comment: Optional[str]
    created_at: str


class Customer(BaseModel):
    id: str
    name: str
    phone: str
    email: Optional[str]
    restaurant_id: str
    created_at: datetime
    message_sent: bool
    message_sent_at: Optional[datetime]
    review_clicked: bool
    review_clicked_at: Optional[datetime]
    feedback_sent: bool

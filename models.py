"""Data models and schemas using Pydantic for structured LLM parsing and tool calls."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class UrgencyLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IssueType(str, Enum):
    BILLING = "billing"
    TECHNICAL_OUTAGE = "technical_outage"
    BUG = "bug"
    FEATURE_REQUEST = "feature_request"
    GENERAL_INQUIRY = "general_inquiry"


class CustomerSentiment(str, Enum):
    ANGRY = "angry"
    FRUSTRATED = "frustrated"
    NEUTRAL = "neutral"
    POSITIVE = "positive"


class NextAction(str, Enum):
    AUTO_RESPOND = "auto_respond"
    ROUTE_TO_SPECIALIST = "route_to_specialist"
    ESCALATE_TO_HUMAN = "escalate_to_human"


class KeyInformation(BaseModel):
    product: str = Field(description="The product or platform surface mentioned.")
    issue_type: IssueType = Field(description="Categorized type of customer issue.")
    customer_sentiment: CustomerSentiment = Field(description="Analyzed sentiment of customer.")
    affected_seats_or_tier: Optional[str] = Field(None, description="Customer plan tier or impact scope.")


class RecommendedResponse(BaseModel):
    suggested_reply: str = Field(description="Drafted response or action note to customer/team.")
    relevant_kb_article_ids: List[str] = Field(default_factory=list, description="List of matched KB article IDs.")


class TriageDecision(BaseModel):
    urgency: UrgencyLevel = Field(description="Assigned ticket urgency.")
    key_info: KeyInformation = Field(description="Extracted metadata.")
    next_action: NextAction = Field(description="Determined operational next action.")
    assigned_team: str = Field(description="Target team or escalation channel (e.g., Tier 1, Billing, DevOps On-Call).")
    response: RecommendedResponse = Field(description="Draft response or resolution steps.")
    reasoning_summary: str = Field(description="Concise summary explaining the triage decision.")


class TicketMessage(BaseModel):
    timestamp_relative: str
    content: str


class CustomerInfo(BaseModel):
    plan_tier: str
    tenure: str
    seats: Optional[int] = None
    region: Optional[str] = None
    previous_tickets_count: int = 0


class TicketInput(BaseModel):
    ticket_id: str
    customer_info: CustomerInfo
    messages: List[TicketMessage]
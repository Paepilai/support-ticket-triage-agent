"""Unit tests for the Support Ticket Triage Agent."""

import pytest
from agent import SupportTriageAgent
from models import CustomerInfo, NextAction, TicketInput, TicketMessage, UrgencyLevel


def test_sample_ticket_structure():
  """Verify ticket input instantiation and Pydantic validation."""
  ticket = TicketInput(
      ticket_id="TEST-001",
      customer_info=CustomerInfo(
          plan_tier="Enterprise", tenure="6 months", seats=10
      ),
      messages=[
          TicketMessage(
              timestamp_relative="10 mins ago",
              content="System error 500 when logging in",
          )
      ],
  )
  assert ticket.ticket_id == "TEST-001"
  assert ticket.customer_info.plan_tier == "Enterprise"
  assert len(ticket.messages) == 1


@pytest.mark.integration
def test_agent_triage_execution():
  """Test agent processing end-to-end (requires OPENAI_API_KEY)."""
  agent = SupportTriageAgent(model_name="gpt-4o")
  ticket = TicketInput(
      ticket_id="TEST-002",
      customer_info=CustomerInfo(plan_tier="Pro", tenure="1 year"),
      messages=[
          TicketMessage(
              timestamp_relative="just now",
              content="Is dark mode supported in Settings?",
          )
      ],
  )
  decision = agent.process_ticket(ticket, "pro_daily")
  assert decision.urgency in [UrgencyLevel.LOW, UrgencyLevel.MEDIUM]
  assert decision.key_info.product != ""
  assert decision.reasoning_summary != ""
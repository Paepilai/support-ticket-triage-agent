"""Agent runtime orchestrating tool calls and structured decision parsing."""

import json
from typing import Dict, Any
from openai import OpenAI
from models import TriageDecision, TicketInput
from tools import TOOLS_SCHEMA, TOOL_MAPPING
from prompts import SYSTEM_TRIAGE_PROMPT


class SupportTriageAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.client = OpenAI()
        self.model_name = model_name

    def process_ticket(self, ticket: TicketInput, customer_db_key: str) -> TriageDecision:
        """Executes tool-calling loop and yields final structured Triage decision."""
        
        messages_str = "\n".join([f"[{m.timestamp_relative}] {m.content}" for m in ticket.messages])
        user_content = (
            f"=== TICKET DATA ===\n"
            f"Ticket ID: {ticket.ticket_id}\n"
            f"Customer DB Key: {customer_db_key}\n"
            f"Customer Meta: Plan={ticket.customer_info.plan_tier}, "
            f"Tenure={ticket.customer_info.tenure}, "
            f"Seats={ticket.customer_info.seats}, "
            f"Region={ticket.customer_info.region}\n\n"
            f"=== CONVERSATION LOG ===\n"
            f"{messages_str}"
        )

        conversation_history = [
            {"role": "system", "content": SYSTEM_TRIAGE_PROMPT},
            {"role": "user", "content": user_content}
        ]

        for _ in range(5):
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=conversation_history,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                temperature=0.0
            )
            
            response_message = response.choices[0].message
            conversation_history.append(response_message)

            if not response_message.tool_calls:
                break

            for tool_call in response_message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                
                if fn_name in TOOL_MAPPING:
                    tool_output = TOOL_MAPPING[fn_name](**fn_args)
                else:
                    tool_output = json.dumps({"error": f"Tool {fn_name} not found"})

                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output
                })

        structured_response = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=conversation_history + [
                {"role": "user", "content": "Now output the complete structured triage decision using the TriageDecision schema."}
            ],
            response_format=TriageDecision,
            temperature=0.0
        )

        return structured_response.choices[0].message.parsed
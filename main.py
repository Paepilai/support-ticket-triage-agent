"""CLI Application executing sample tickets and printing formatted triage reports."""

import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent import SupportTriageAgent
from models import CustomerInfo, TicketInput, TicketMessage

console = Console()


def get_sample_tickets():
    return [
        (
            TicketInput(
                ticket_id="TCK-001",
                customer_info=CustomerInfo(
                    plan_tier="Free plan (upgrade attempted)",
                    tenure="4 months",
                    previous_tickets_count=0,
                ),
                messages=[
                    TicketMessage(
                        timestamp_relative="3 hours ago",
                        content=(
                            "My payment failed when I tried to upgrade to Pro."
                            " Can you check what's wrong?"
                        ),
                    ),
                    TicketMessage(
                        timestamp_relative="2 hours ago",
                        content=(
                            "I tried again with a different card. Now I see TWO"
                            " pending charges but my account still shows Free"
                            " plan??"
                        ),
                    ),
                    TicketMessage(
                        timestamp_relative="1 hour ago",
                        content=(
                            "Okay this is getting ridiculous. Just checked my"
                            " bank app - I have THREE charges of $29.99 now."
                            " None of them refunded. And I STILL don't have Pro"
                            " access."
                        ),
                    ),
                    TicketMessage(
                        timestamp_relative="just now",
                        content=(
                            "HELLO?? Is anyone there???\nI need this fixed NOW."
                            " I have a presentation in 2 hours and I need the"
                            " Pro export features. If these charges aren't"
                            " reversed by end of day I'm disputing all of them"
                            " with my bank."
                        ),
                    ),
                ],
            ),
            "free_user_1",
        ),
        (
            TicketInput(
                ticket_id="TCK-002",
                customer_info=CustomerInfo(
                    plan_tier="Enterprise",
                    tenure="8 months",
                    seats=45,
                    region="Thailand",
                    previous_tickets_count=0,
                ),
                messages=[
                    TicketMessage(
                        timestamp_relative="2 hours ago",
                        content="ระบบเข้าไม่ได้ครับ ขึ้น error 500",
                    ),
                    TicketMessage(
                        timestamp_relative="1.5 hours ago",
                        content=(
                            "ลองหลายเครื่องแล้ว ทั้ง Chrome, Safari, Firefox"
                            " ผลเหมือนกันหมด เพื่อนร่วมงานก็เข้าไม่ได้เหมือนกัน"
                        ),
                    ),
                    TicketMessage(
                        timestamp_relative="45 mins ago",
                        content=(
                            "ตอนนี้ลูกค้าโวยเข้ามาเยอะมาก เรามี demo"
                            " กับลูกค้ารายใหญ่บ่ายนี้ ถ้าระบบไม่กลับมา deal"
                            " นี้อาจจะหลุด"
                        ),
                    ),
                    TicketMessage(
                        timestamp_relative="just now",
                        content=(
                            "เช็ค status.company.com แล้ว บอกว่า all systems"
                            " operational แต่เราใช้งานไม่ได้จริงๆ"
                            " ช่วยเช็คให้หน่อยได้ไหมครับ region Asia"
                            " มีปัญหาหรือเปล่า?"
                        ),
                    ),
                ],
            ),
            "enterprise_th",
        ),
        (
            TicketInput(
                ticket_id="TCK-003",
                customer_info=CustomerInfo(
                    plan_tier="Pro",
                    tenure="5 months",
                    previous_tickets_count=0,
                ),
                messages=[
                    TicketMessage(
                        timestamp_relative="2 days ago",
                        content="Hey, just wondering if you support dark mode? No rush 😊",
                    ),
                    TicketMessage(
                        timestamp_relative="1 day ago",
                        content=(
                            "Thanks for the reply! Oh nice, so it's in Settings"
                            " > Appearance. Found it! But hmm I'm on Pro plan"
                            " and I only see 'Light' and 'System Default'"
                            " options. No dark mode toggle?"
                        ),
                    ),
                    TicketMessage(
                        timestamp_relative="1 day ago, 3 hours later",
                        content=(
                            "Okay so I switched to 'System Default' and my Mac"
                            " is set to dark mode, but your app still shows"
                            " light theme. Is this a bug or am I missing"
                            " something?"
                        ),
                    ),
                    TicketMessage(
                        timestamp_relative="today",
                        content=(
                            "Also random question while I have you - is there a"
                            " way to schedule dark mode? Like auto-switch at"
                            " 6pm? Some apps have that. Would be cool if you"
                            " guys added it 👀"
                        ),
                    ),
                ],
            ),
            "pro_daily",
        ),
    ]


def run_agent():
  if not os.getenv("OPENAI_API_KEY"):
    console.print(
        "[bold red]Error: OPENAI_API_KEY environment variable is missing![/bold red]"
    )
    return

  agent = SupportTriageAgent(model_name="gpt-4o")
  sample_tickets = get_sample_tickets()

  console.print(
      "[bold green]Starting Ooca AI Support Ticket Triage Agent...[/bold green]\n"
  )

  for ticket, db_key in sample_tickets:
    console.print(f"[bold cyan]Processing Ticket: {ticket.ticket_id}[/bold cyan]")
    decision = agent.process_ticket(ticket, db_key)

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property", style="dim")
    table.add_column("Value")

    table.add_row("Urgency", decision.urgency.value.upper())
    table.add_row("Next Action", decision.next_action.value)
    table.add_row("Assigned Team", decision.assigned_team)
    table.add_row("Issue Type", decision.key_info.issue_type.value)
    table.add_row(
        "Customer Sentiment", decision.key_info.customer_sentiment.value
    )
    table.add_row("Matched KB IDs", ", ".join(decision.response.relevant_kb_article_ids) or "None")

    console.print(table)

    console.print(
        Panel(
            f"[bold]Reasoning:[/bold] {decision.reasoning_summary}\n\n"
            f"[bold]Suggested Response/Action:[/bold]\n{decision.response.suggested_reply}",
            title=f"Triage Result - {ticket.ticket_id}",
            border_style="blue",
        )
    )
    console.print("-" * 80)


if __name__ == "__main__":
  run_agent()
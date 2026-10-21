# Support Ticket Triage Agent

An enterprise-grade AI agent built with **Python, OpenAI GPT-4o, and Pydantic V2** that triages multi-turn support tickets, retrieves relevant context, extracts structured metadata, and recommends the appropriate next action.

It supports Thai and English tickets and uses customer history, internal knowledge, and system-status checks to make grounded triage decisions.

## Key Features

- **Structured outputs** — Uses OpenAI's `beta.chat.completions.parse` with Pydantic V2 models to validate triage results against a defined schema.
- **Dynamic tool calling** — Retrieves context through three tools: `check_customer_history`, `lookup_knowledge_base`, and `check_system_status`.
- **Multilingual support** — Handles Thai and English tickets while preserving the ticket's language context.
- **Safety and escalation** — Escalates high-risk cases such as critical system outages, financial or chargeback disputes, and urgent client deadlines.
- **Modular design** — Separates models, tools, prompts, agent logic, and the application runner to support testing and future extension.

## Architecture & Evaluation

For the detailed technical report, see **[WRITEUP.md](./WRITEUP.md)**. It covers:

- Architecture decisions and design rationale
- Failure modes and mitigation strategies
- Extensibility and scalability
- Production evaluation and observability

## Project Structure

```text
support-ticket-triage-agent/
├── README.md
├── WRITEUP.md
├── pytest.ini
├── requirements.txt
├── mock_db.py
├── models.py
├── tools.py
├── prompts.py
├── agent.py
├── main.py
└── test_agent.py
```

## Setup & Installation

### 1. Clone the repository

```bash
git clone <github-repo-url>
cd support-ticket-triage-agent
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Set `OPENAI_API_KEY` in your environment. Replace the placeholder with your own key.

**macOS / Linux**

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

**Windows (PowerShell)**

```powershell
$env:OPENAI_API_KEY="your-openai-api-key-here"
```

## Run the Application

Run the agent against the sample customer tickets and print the terminal reports:

```bash
python main.py
```

## Run Tests

Run the automated unit tests:

```bash
pytest test_agent.py
```

## Technology Stack

- Python
- OpenAI GPT-4o
- Pydantic V2
- pytest

---

For implementation details and the evaluation framework, start with **[WRITEUP.md](./WRITEUP.md)**.

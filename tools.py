"""Tools schema definitions and implementations for the OpenAI agent."""

import json
from typing import Dict, Any, List
from mock_db import MOCK_KNOWLEDGE_BASE, MOCK_CUSTOMER_DB


def lookup_knowledge_base(query: str, category: str = None) -> str:
    """Searches the knowledge base for articles relevant to the query keyword or category."""
    results = []
    query_terms = query.lower().split()
    
    for item in MOCK_KNOWLEDGE_BASE:
        text = f"{item['title']} {item['content']} {item['category']}".lower()
        if any(term in text for term in query_terms) or (category and category.lower() in item['category'].lower()):
            results.append({
                "id": item["id"],
                "title": item["title"],
                "content": item["content"]
            })
            
    if not results:
        results = MOCK_KNOWLEDGE_BASE  # Fallback to full list if no direct term match
        
    return json.dumps(results, ensure_ascii=False)


def check_customer_history(customer_id: str) -> str:
    """Fetches customer account status, SLA tier, billing details, and support records."""
    record = MOCK_CUSTOMER_DB.get(customer_id, {
        "status": "Standard Record",
        "details": f"No active alerts found for customer ID: {customer_id}"
    })
    return json.dumps(record, ensure_ascii=False)

def check_system_status(region: str = "global", service_name: str = None) -> str:
    """Checks live regional system status and active incidents from internal telemetry monitoring."""
    status_db = {
        "asia": {
            "status": "DEGRADED",
            "active_incident": "INC-4092: High packet loss and HTTP 500 spikes on Asia-East edge routing nodes.",
            "impacted_services": ["API Gateway", "Web Portal"]
        },
        "global": {
            "status": "OPERATIONAL",
            "active_incident": None
        }
    }
    
    region_key = region.lower() if region.lower() in status_db else "global"
    return json.dumps(status_db[region_key], ensure_ascii=False)

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "lookup_knowledge_base",
            "description": "Search internal knowledge base articles, FAQs, and troubleshooting guides.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keywords or search phrases describing the issue (e.g. 'dark mode', 'payment failed 500 error')."
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional category filter: billing, technical, features."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_customer_history",
            "description": "Retrieve customer subscription status, SLA terms, billing flags, or account tier details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Identifier key for customer lookup (e.g. 'free_user_1', 'enterprise_th', 'pro_daily')."
                    }
                },
                "required": ["customer_id"]
            }
        }
    },
{
        "type": "function",
        "function": {
            "name": "check_system_status",
            "description": "Query real-time infrastructure status, regional edge health, or active telemetry incidents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "region": {
                        "type": "string",
                        "description": "Geographic region to inspect (e.g., 'asia', 'us-east', 'global')."
                    },
                    "service_name": {
                        "type": "string",
                        "description": "Optional specific service name (e.g., 'auth', 'database', 'api')."
                    }
                },
                "required": ["region"]
            }
        }
    }
]

TOOL_MAPPING = {
    "lookup_knowledge_base": lookup_knowledge_base,
    "check_customer_history": check_customer_history,
    "check_system_status": check_system_status
}
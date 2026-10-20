"""Mock databases for Knowledge Base (KB) and Customer Accounts."""

MOCK_KNOWLEDGE_BASE = [
    {
        "id": "KB-101",
        "title": "Multiple Pending Card Charges & Failed Tier Upgrade",
        "category": "billing",
        "content": (
            "When a payment fails or is retried multiple times, banks place temporary pending authorization holds. "
            "These holds usually drop off within 24-48 hours. If the subscription tier does not update to Pro immediately, "
            "do NOT re-try. Manual provisioning or automated clearing is required by Billing. Escalate to Billing Team if pending > 2."
        )
    },
    {
        "id": "KB-202",
        "title": "HTTP 500 Internal Server Errors & Regional Outages",
        "category": "technical",
        "content": (
            "HTTP 500 across multiple browsers/users indicates a backend or edge routing disruption. "
            "Status page (status.company.com) may have a reporting latency of up to 15 minutes. "
            "For Enterprise accounts experiencing downtime during business hours, trigger High/Critical incident protocol immediately "
            "and alert the DevOps/Asia-Pacific On-Call team."
        )
    },
    {
        "id": "KB-303",
        "title": "Dark Mode Setup and OS Theme Syncing",
        "category": "features",
        "content": (
            "To enable Dark Mode: Go to Settings > Appearance. Selecting 'System Default' syncs with OS dark theme. "
            "If OS dark theme is enabled on macOS/Windows but the app remains Light, restart the app or clear web cache. "
            "Note: Scheduled auto-switching (e.g., at 6 PM) is not currently supported; submit as a Feature Request."
        )
    }
]

MOCK_CUSTOMER_DB = {
    "free_user_1": {
        "tier": "Free",
        "billing_status": "Failed Authorization / 3 Pending Holds ($29.99 x 3)",
        "account_flag": "Payment Blocked",
        "support_tier": "Standard"
    },
    "enterprise_th": {
        "tier": "Enterprise",
        "seats": 45,
        "region": "Asia/Bangkok",
        "sla_tier": "24/7 Priority Incident Response (SLA < 15 mins)",
        "assigned_account_manager": "Somchai P."
    },
    "pro_daily": {
        "tier": "Pro",
        "daily_active": True,
        "support_tier": "Priority Email",
        "account_status": "Active"
    }
}
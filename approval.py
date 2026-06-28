
"""Purpose:Implements Human-in-the-Loop (HITL).Certain sensitive customer requests require
human approval before the AI can respond."""
from state import SupportState
from rich.console import Console
from rich.panel import Panel
# ==========================================================
# Check Approval Requirement
# ==========================================================
def approval_node(state: SupportState) -> dict:
    """Checks whether the customer's request requires human approval. """
    query = state["user_query"].lower()
    approval_keywords = [
        "refund",
        "cancel subscription",
        "subscription cancellation",
        "delete account",
        "close account",
        "compensation",
        "manager",
        "escalate"
    ]
    requires_approval = any(
        keyword in query
        for keyword in approval_keywords
    )
    return {
        "approval_required": requires_approval
    }
# ==========================================================
# Human Approval
# ==========================================================
def human_approval_node(state: SupportState) -> dict:
    """Simulates human approva"""
    console = Console()
    console.print(
    Panel(
        f"[bold red]{state['user_query']}[/bold red]",
        title="⚠ Human Approval Required",
        border_style="red"
    )
)
    print(f"\nCustomer Request:\n{state['user_query']}")
    choice = input("\nApprove request? (yes/no): ").strip().lower()
    approved = choice == "yes"
    if approved:
        response = (
            "Your request has been approved by our support team."
        )
    else:
        response = (
            "Your request has been rejected by our support team."
        )
    return {
        "approved": approved,
        "response": response
    }
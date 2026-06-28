"""Purpose:
Creates the complete LangGraph workflow for the
AI-Powered Customer Support Automation System."""
from langgraph.graph import StateGraph, START, END
from state import SupportState
from classifier import classify_intent
from rag import rag_node
from agents import (
    sales_agent,
    technical_agent,
    billing_agent,
    account_agent,
)
from memory import (
    memory_node,
    memory_recall_node
)
from approval import (
    approval_node,
    human_approval_node
)
from supervisor import supervisor_node
# ==========================================================
# Intent Router
# ==========================================================
def route_intent(state: SupportState) -> str:
    """
    Routes the workflow based on
    the predicted intent.
    """
    intent = state["intent"]
    if intent == "Sales":
        return "sales"
    elif intent == "Technical":
        return "technical"
    elif intent == "Billing":
        return "billing"
    elif intent == "Account":
        return "account"
    elif intent == "Memory":
        return "memory_recall"
    return "technical"
# ==========================================================
# Approval Router
# ==========================================================
def route_approval(state: SupportState) -> str:
    """
    Routes depending on whether
    human approval is required.
    """
    if state["approval_required"]:
        return "human"
    return "supervisor"
# ==========================================================
# Build Graph
# =========================================================
graph_builder = StateGraph(SupportState)
# ==========================================================
# Add Nodes
# =========================================================
graph_builder.add_node("classifier", classify_intent)
graph_builder.add_node("rag", rag_node)
graph_builder.add_node("sales", sales_agent)
graph_builder.add_node("technical", technical_agent)
graph_builder.add_node("billing", billing_agent)
graph_builder.add_node("account", account_agent)
graph_builder.add_node("memory", memory_node)
graph_builder.add_node("memory_recall", memory_recall_node)
graph_builder.add_node("approval", approval_node)
graph_builder.add_node("human", human_approval_node)
graph_builder.add_node("supervisor", supervisor_node)
# ==========================================================
# Start
# ==========================================================
graph_builder.add_edge(
    START,
    "classifier"
)
graph_builder.add_edge(
    "classifier",
    "rag"
)
# ==========================================================
# Intent Routing
# ==========================================================
graph_builder.add_conditional_edges(
    "rag",
    route_intent,
    {
        "sales": "sales",
        "technical": "technical",
        "billing": "billing",
        "account": "account",
        "memory_recall": "memory_recall",
    },
)
# ==========================================================
# Agent Flow
# ==========================================================
graph_builder.add_edge(
    "sales",
    "memory"
)
graph_builder.add_edge(
    "technical",
    "memory"
)
graph_builder.add_edge(
    "billing",
    "memory"
)
graph_builder.add_edge(
    "account",
    "memory"
)
# ==========================================================
# Memory Recall
# ==========================================================
graph_builder.add_edge(
    "memory_recall",
    "supervisor"
)
# ==========================================================
# Memory
# ==========================================================
graph_builder.add_edge(
    "memory",
    "approval"
)
# ==========================================================
# Approval Routing
# ==========================================================
graph_builder.add_conditional_edges(
    "approval",
    route_approval,
    {
        "human": "human",
        "supervisor": "supervisor",
    },
)
graph_builder.add_edge(
    "human",
    "supervisor"
)
graph_builder.add_edge(
    "supervisor",
    END
)
# ==========================================================
# Compile
# ==========================================================
graph = graph_builder.compile()
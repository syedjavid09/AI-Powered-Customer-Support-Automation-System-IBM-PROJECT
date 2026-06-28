"""Purpose:
Contains all department-specific support agents.
Each agent:
- Receives the shared SupportState
- Uses the LLM to generate a response
- Returns the updated state."""
from state import SupportState
from llm import llm
# ==========================================================
# SALES AGENT
# ==========================================================
def sales_agent(state: SupportState) -> dict:
    """Handles sales-related customer queries."""
    prompt = f"""You are the Sales Support Agent for ABC Technologies.
Answer ONLY using the retrieved company documents.
Rules:
- Use ONLY the retrieved context.
- Do NOT make up pricing.
- Do NOT invent plans.
- Do NOT add information that is not present.
- If the answer is not available in the context, reply:
  "I couldn't find that information in the company documentation."
Retrieved Context:{state["rag_context"]}
Customer Question:{state["user_query"]}
Return a professional and friendly response.
"""
    response = llm.invoke(prompt)
    return {
        "response": response.content
    }
# ==========================================================
# TECHNICAL AGENT
# ==========================================================
def technical_agent(state: SupportState) -> dict:
    """Handles technical support requests."""
    prompt = f"""You are the Technical Support Agent for ABC Technologies.
Answer ONLY using the retrieved technical documentation.
Rules:
- Use ONLY the retrieved context.
- Do NOT invent troubleshooting steps.
- If the answer is not available in the context, reply:
  "I couldn't find that information in the technical documentation."
Retrieved Context:{state["rag_context"]}
Customer Question:{state["user_query"]}
Provide clear step-by-step guidance whenever possible."""
    response = llm.invoke(prompt)
    return {
        "response": response.content
    }
# ==========================================================
# BILLING AGENT
# ==========================================================
def billing_agent(state: SupportState) -> dict:
    """Handles billing-related requests."""
    prompt = f"""You are the Billing Support Agent for ABC Technologies.
Answer ONLY using the retrieved billing information.
Rules:
- Use ONLY the retrieved context.
- Do NOT invent refund policies.
- Do NOT invent payment information.
- If the answer is not available in the context, reply:
  "I couldn't find that information in the company documentation."
Retrieved Context:{state["rag_context"]}
Customer Question:{state["user_query"]}
Return a professional response."""
    response = llm.invoke(prompt)
    return {
        "response": response.content
    }
# ==========================================================
# ACCOUNT AGENT
# ==========================================================
def account_agent(state: SupportState) -> dict:
    """Handles account management requests."""
    query = state["user_query"].lower()
    # Handle user introducing their name
    if query.startswith("my name is"):
        name = state["user_query"][10:].strip().title()
        return {
            "response": f"Nice to meet you💕, {name}! I'll remember your name during this conversation. How can I assist you today?"
        }
    prompt = f"""
You are the Account Support Agent for ABC Technologies.
Answer ONLY using the retrieved company documentation.
Rules:
- Use ONLY the retrieved context.
- Do NOT invent company policies.
- If the answer is not available in the context, reply:
  "I couldn't find that information in the company documentation."
Retrieved Context:{state["rag_context"]}
Customer Question:{state["user_query"]}
Return a helpful and professional response."""
    response = llm.invoke(prompt)
    return {
        "response": response.content
    }
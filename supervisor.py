"""
Purpose:
Reviews and improves the response generated
by the support agents before sending it
to the customer.
"""
from state import SupportState
from llm import llm
# ==========================================================
# Supervisor Agent
# ==========================================================
def supervisor_node(state: SupportState) -> dict:
    """
    Reviews the generated response and improves
    grammar, clarity and professionalism
    without changing the business decision.
    """
    prompt = f"""
You are the Customer Support Supervisor for ABC Technologies.
Your responsibility is ONLY to improve the quality of the response.
Rules:
1. Improve grammar.
2. Improve clarity.
3. Make the response professional.
4. Make the response polite.
5. Keep the response concise.

IMPORTANT:

- DO NOT change the business decision.
- DO NOT change approval status.
- DO NOT change rejection status.
- DO NOT add new information.
- DO NOT remove important information.
- DO NOT invent company policies.
- DO NOT invent pricing.
- DO NOT change any facts.

Customer Question:{state["user_query"]}
Current Response:{state["respose"]}
Return ONLY the improved response.
"""
    response = llm.invoke(prompt)
    return {
        "response": response.content
    }
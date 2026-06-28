"""Purpose:Classifies the customer's query into the correct department.
Possible intents:
- Sales
- Technical
- Billing
- Account
- Memory"""
from state import SupportState
from llm import llm
from rich import print 
def classify_intent(state: SupportState) -> dict:
    """Classifies the user's query into one of the predefined intents
    Args:state: Shared LangGraph state.
    Returns:Dictionary containing the predicted intent."""
    # Extract the customer's query
    query = state["user_query"]
    query_lower = query.lower()
    if query_lower.startswith("my name is"):
        return {
            "intent": "Account"
    }
    # Prompt for intent classification
    prompt = f"""You are an AI Intent Classification Agent for ABC Technologies.your job is ONLY to classify the customer's query.
Choose ONLY ONE category from the following:
- Sales
- Technical
- Billing
- Account
- Memory
Rules:

Sales:
- Pricing
- Plans
- Subscription plans
- Cost
- Product features
- Product information

Technical:
- Application crashes
- Software errors
- Installation issues
- Configuration issues
- Login server problems

Billing:
- Refund requests
- Invoice requests
- Payment failed
- Subscription payment issues
- Credit card issues

Account:
- Forgot password
- Password reset
- Profile update
- Change email
- Account activation
- Account deactivation
- Delete account

Memory:
ONLY classify as Memory if the customer is ASKING about previous conversations.
Examples:
What was my previous issue?
What is my name?
What did I ask before?
Do you remember me?
Do NOT classify statements as Memory.
Examples
My name is Manoj.
I have a billing issue
I love coding.
I want to buy a subscription
Customer Query:{query}
Return ONLY ONE WORD.
Example outputs:
Sales
Technical
Billing
Account
Memory
"""
    # Ask the LLM to classify
    response = llm.invoke(prompt)
    # Clean the output
    intent = response.content.strip()
    from rich import print
    print(f"[bold blue]🧠 Intent:[/bold blue] [green]{intent}[/green]")
    # Return the updated state
    return {
        "intent": intent
    }
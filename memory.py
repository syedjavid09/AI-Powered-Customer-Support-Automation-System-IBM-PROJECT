"""Purpose:
Stores and retrieves customer conversations
using SQLite.
"""
import sqlite3
from rich import print
from state import SupportState
from llm import llm
# ==========================================================
# Database Connection
# ==========================================================
DATABASE = "Database/memory.db"
# ==========================================================
# Create Database
# ==========================================================
def initialize_database():
    """
    Creates the conversation table
    if it doesn't already exist.
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT,
            ai_response TEXT
        )
    """)
    connection.commit()
    connection.close()
# ==========================================================
# Save Conversation
# ==========================================================
def save_conversation(state: SupportState) -> dict:
    """
    Saves the latest conversation
    into SQLite.
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO conversations
        (user_query, ai_response)
        VALUES (?, ?)
        """,
        (
            state["user_query"],
            state["response"]
        )
    )
    connection.commit()
    connection.close()
    return {}
# ==========================================================
# Search Conversation
# ==========================================================
def search_memory() -> str:
    """
    Retrieves the latest customer conversations
    from SQLite.
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT user_query,
               ai_response
        FROM conversations
        ORDER BY id DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    connection.close()
    if not rows:
        return "No previous conversation found."
    memory = ""
    for user, ai in reversed(rows):
        memory += f"""
Customer:{user}
Support Agent:{ai}
"""
    return memory
# ==========================================================
# LangGraph Memory Node
# ==========================================================
def memory_node(state: SupportState) -> dict:
    """
    Saves the current conversation
    into SQLite.
    """
    save_conversation(state)
    return {}
#
def memory_recall_node(state: SupportState) -> dict:
    """
    Retrieves previous conversation information
    directly from SQLite.
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT user_query
        FROM conversations
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    connection.close()
    query = state["user_query"].lower()
    # ======================================================
    # Recall Previous Support Issue
    # ======================================================
    if (
    "previous" in query
    and (
        "issue" in query
        or "problem" in query
        or "support" in query
    )
):
     response = None
    for row in rows:
        previous_query = row[0].lower()
        if "billing" in previous_query:
            response = "Your previous support issue was related to Billing."
            break
        elif "password" in previous_query:
            response = "Your previous support issue was related to your Account password."
            break
        elif "login" in previous_query:
            response = "Your previous support issue was related to Login."
            break
        elif "technical" in previous_query:
            response = "Your previous support issue was related to Technical Support."
            break
        elif "refund" in previous_query:
            response = "Your previous support issue was related to a Refund request."
            break
        print("[bold cyan]🧠 Memory[/bold cyan] [green]Previous conversation found[/green]")
        return {
            "response": response
        }
    return {
        "response": "I couldn't find any previous support issue."
    }
    # ======================================================
    # Recall Customer Name
    # ======================================================
    if "what is my name" in query:
        for row in rows:
            previous_query = row[0]
            if previous_query.lower().startswith("my name is"):
                name = previous_query[10:].strip().title()
                print("[bold cyan]🧠 Memory[/bold cyan] [green]Customer information retrieved[/green]")
                return {
                   "response": f"Your name is {name}."
                }
        return {
            "response": "I couldn't find your name in the previous conversations."
        }
    # ======================================================
    # Default Memory Search
    # ======================================================
    memory = search_memory()
    prompt = f"""
You are the Memory Assistant for ABC Technologies.
Previous Conversation History:{memory}
Current Question:{state["user_query"]}
Answer ONLY using the previous conversation history.
If the answer is not available, reply:
"I couldn't find that information in the previous conversations."
Return ONLY the answer.
"""
    response = llm.invoke(prompt)
    return {
        "response": response.content
    }

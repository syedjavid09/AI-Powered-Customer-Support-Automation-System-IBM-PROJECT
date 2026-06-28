"""Purpose:
Entry point of the AI-Powered Customer SupporAutomation System."""
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.markdown import Markdown
import os
from graph import graph
from memory import initialize_database
from rag import create_vector_store
# ==========================================================
# Initialize Project
# ==========================================================
console = Console()
console.print(
    Panel.fit(
        "[bold cyan]🤖 AI-Powered Customer Support Automation System[/bold cyan]",
        border_style="cyan"
    )
)
console.print("[green]✓ Initializing SQLite Database...[/green]")
initialize_database()
console.print("[green]✓ Checking Vector Database...[/green]")
if not os.path.exists("Database/chroma_db"):
    console.print("[yellow]Creating Vector Database...[/yellow]")
    create_vector_store()
else:
    console.print("[green]✓ Vector Database Ready[/green]")
console.print("[bold green]✓ System Ready[/bold green]")
console.print(Rule(style="cyan"))
# =========================================================
# Chat Loop
# ==========================================================
while True:
    console.print("\n[bold yellow]Customer[/bold yellow]")
    user_query = input("➜ ")
    if user_query.lower() in ["exit", "quit"]:
        print("\nThank you for using ABC Customer Support.")
        break
    # Initial LangGraph State
    initial_state = {
        "user_query": user_query,
        "intent": "",
        "rag_context": "",
        "response": "",
        "approval_required": False,
        "approved": False,
        "history": []
    }
    # Execute LangGraph Workflow
    result = graph.invoke(initial_state)
    console.print()
    console.print(
    Panel(
        Markdown(result["response"]),
        title="[bold green]Support Agent[/bold green]",
        border_style="green"
    )
)
console.print(Rule(style="cyan"))
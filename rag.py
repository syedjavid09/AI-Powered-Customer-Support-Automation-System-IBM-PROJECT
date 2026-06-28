"""Purpose:
Loads company documents, creates embeddings,
stores them in ChromaDB, and retrieves
relevant information for customer support."""
import os
from rich import print
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
# ==========================================================
# Embedding Model
# ==========================================================
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
# ==========================================================
# Load Documents
# ==========================================================
def load_documents():
    """
    Loads all text files from the Documents folder.
    """
    documents = []
    for file_name in os.listdir("Rag Documents"):
        if file_name.endswith(".txt"):
            print(f"Loading: {file_name}")
            loader = TextLoader(
                os.path.join("Rag Documents", file_name),
                encoding="utf-8"
            )
            documents.extend(loader.load())
    print(f"\nTotal Documents Loaded: {len(documents)}\n")
    return documents
# ==========================================================
# Split Documents
# =========================================================
def split_documents(documents):
    """
    Splits documents into chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    print(f"Total Chunks Created: {len(chunks)}\n")
    return chunks
# ==========================================================
# Create Vector Store
# ==========================================================
def create_vector_store():
    """
    Creates the Chroma Vector Database.
    """
    documents = load_documents()
    chunks = split_documents(documents)
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="Database/chroma_db"
    )
    print("Vector Database Created Successfully!\n")
    return vector_db
# ==========================================================
# Retrieve Context
# ==========================================================
def retrieve_context(query: str) -> str:
    """
    Retrieves relevant context from ChromaDB.
    """
    vector_db = Chroma(
        persist_directory="Database/chroma_db",
        embedding_function=embedding_model
    )
    retriever = vector_db.as_retriever(
        search_kwargs={"k": 1}
    )
    documents = retriever.invoke(query)
    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )
    print("[bold magenta]📚 RAG[/bold magenta] [green]Relevant documents retrieved[/green]")
    return context

# ==========================================================
# LangGraph Node
# ==========================================================
from state import SupportState
def rag_node(state: SupportState) -> dict:

    context = retrieve_context(state["user_query"])
    return {
        "rag_context": context
    }

import os
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

# Setup
vectorDB = str(Path(__file__).parent.parent / "vectorstore")
embeddings = HuggingFaceEmbeddings(model_name="multi-qa-MiniLM-L6-cos-v1")
vectors = Chroma(persist_directory=vectorDB, embedding_function=embeddings)
retriever = vectors.as_retriever()
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

SYSTEM_PROMPT = """
You are CurryBot 🍛 — a friendly Indian food assistant.
You know recipes from Maharashtra, South India, Gujarat, Punjab and Bengal.
Use ONLY the context below to answer — do not use your own knowledge.
Never say the context is incorrect — trust it completely.
Always include: recipe name, ingredients, steps, cost in Rs, time, one tip.
If asked in Hindi or Marathi, reply in that language.

Context:
{context}
"""

history = []

def chat(question: str) -> str:
    past_questions = "\n".join(m["content"] for m in history if m["role"] == "user")
    search_query = past_questions + "\n" + question

    docs = retriever.invoke(search_query)
    context = "\n\n".join(doc.page_content for doc in docs)

    messages = [SystemMessage(content=SYSTEM_PROMPT.format(context=context))]

    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=question))

    response = llm.invoke(messages)

    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": response.content})

    return response.content


if __name__ == "__main__":
    print("🍛 CurryBot is ready!\n")

    print(f"Q: Tell me how to make Misal Pav")
    print(f"A: {chat('Tell me how to make Misal Pav')}\n")
    print("="*60)

    print(f"Q: How much does it cost?")
    print(f"A: {chat('How much does it cost?')}\n")
    print("="*60)

    print(f"Q: Can I make it vegan?")
    print(f"A: {chat('Can I make it vegan?')}\n")
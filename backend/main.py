from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import chat, history

app = FastAPI(title="curryBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@app.get("/")
def home():
    return {"message": "CurryBot API is running! 🍛"}

@app.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    answer = chat(request.question)
    return ChatResponse(answer=answer)

@app.post("/reset")
def reset():
    history.clear()
    return {"message": "Chat history cleared! 🗑️"}
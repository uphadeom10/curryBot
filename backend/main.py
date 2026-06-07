from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag import chat, history

app = FastAPI(title="curryBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Request model — what frontend sends
class ChatRequest(BaseModel):
    question: str

# Response model — what backend returns
class ChatResponse(BaseModel):
    answer: str

# GET / — health check
@app.get("/")
def home():
    return {"message": "CurryBot API is running! 🍛"}

# POST /chat — main chat endpoint
@app.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    answer = chat(request.question)
    return ChatResponse(answer=answer)



# POST /reset — clear chat history
@app.post("/reset")
def reset():
    history.clear()
    return {"message": "Chat history cleared! 🗑️"}
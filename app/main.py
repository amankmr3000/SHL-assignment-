from fastapi import FastAPI
from .models import ChatRequest, ChatResponse
from .catalog import load_catalog
from .retriever import Retriever
from .agent import answer

app = FastAPI(title="SHL Conversational Assessment Recommender")
catalog = load_catalog("data/catalog.json")
retriever = Retriever(catalog)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return answer(req.messages, retriever)

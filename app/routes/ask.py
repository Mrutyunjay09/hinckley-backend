from fastapi import APIRouter
from pydantic import BaseModel
from app.prompt_parser import interpret_query

router = APIRouter()

class AskRequest(BaseModel):
    prompt: str

@router.post("/ask")
async def ask_route(payload: AskRequest):
    response = await interpret_query(payload.prompt)
    return {"answer": response}

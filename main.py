from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model
class Protocol(BaseModel):
    id: int
    name: str
    department_id: int

# DB connection utility
async def get_connection():
    db_port_str = os.getenv("DB_PORT")
    if not db_port_str:
        raise ValueError("DB_PORT is not set in .env")

    return await asyncpg.connect(
        host=os.getenv("DB_HOST"),
        port=int(db_port_str),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.get("/", tags=["Health"])
def health_check() -> dict:
    return {"status": "✅ Server is up and running"}

@app.get("/protocols", response_model=List[Protocol], tags=["Protocols"])
async def get_protocols() -> List[Protocol]:
    try:
        conn = await get_connection()
        rows = await conn.fetch("SELECT id, name, department_id FROM protocol;")
        await conn.close()

        return [Protocol(**dict(row)) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AskRequest(BaseModel):
    prompt: str

from app.prompt_parser import interpret_query

@app.post("/ask", tags=["AI"])
async def ask_route(payload: AskRequest):
    response = await interpret_query(payload.prompt)
    return {"answer": response}

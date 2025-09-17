from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)  # disable Swagger & OpenAPI

# --- Database setup ---
DB_FILE = "chats.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT,
    message_type TEXT,
    content TEXT
)
""")
conn.commit()

# --- Models ---
class Message(BaseModel):
    type: str
    content: str

class Query(BaseModel):
    chat_id: str
    messages: List[Message]

# --- Chat endpoint ---
@app.post("/chat")
async def assistant(query: Query):
    last_message = query.messages[-1].content.strip()

    response = {
        "message": None,
        "base_random_keys": None,
        "member_random_keys": None
    }

    if last_message.lower() == "ping":
        response["message"] = "pong"
    elif last_message.startswith("return base random key:"):
        key = last_message.replace("return base random key:", "").strip()
        response["base_random_keys"] = [key]
    elif last_message.startswith("return member random key:"):
        key = last_message.replace("return member random key:", "").strip()
        response["member_random_keys"] = [key]

    # Save all messages to DB
    for msg in query.messages:
        cursor.execute(
            "INSERT INTO chats (chat_id, message_type, content) VALUES (?, ?, ?)",
            (query.chat_id, msg.type, msg.content)
        )
    conn.commit()

    return response

# --- Retrieve all chats ---
@app.get("/chats")
async def get_chats():
    cursor.execute("SELECT chat_id, message_type, content FROM chats")
    rows = cursor.fetchall()
    return {
        "chats": [{"chat_id": r[0], "type": r[1], "content": r[2]} for r in rows]
    }

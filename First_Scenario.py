from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)  # disable Swagger & OpenAPI

# Models
class Message(BaseModel):
    type: str
    content: str

class Query(BaseModel):
    chat_id: str
    messages: List[Message]

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

    # Log request and response
    logger.info(f"Request: {query.dict()}")
    logger.info(f"Response: {response}")

    return response

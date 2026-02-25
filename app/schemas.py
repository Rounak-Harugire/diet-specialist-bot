from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: str  # This helps us track history for specific users
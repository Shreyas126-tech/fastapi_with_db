from pydantic import BaseModel
from datetime import datetime

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."

class AIResponse(BaseModel):
    response: str

class ChatHistoryResponse(BaseModel):
    id: int
    prompt: str
    response: str
    timestamp: datetime

    class Config:
        from_attributes = True

class ImageRequest(BaseModel):
    prompt: str

class ImageResponse(BaseModel):
    image_url: str

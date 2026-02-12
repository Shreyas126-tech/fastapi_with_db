from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.ai_response import get_completion
from schemas.ai_response_schemas import AIRequest, AIResponse, ChatHistoryResponse
from db import get_db
from models import ChatHistory
from utils.auth_deps import get_current_user_id
from typing import List

router = APIRouter()


@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Get response from AI model and save to history."""
    try:
        response = get_completion(request.message, request.system_prompt)
        
        # Save to history
        new_history = ChatHistory(
            user_id=user_id,
            prompt=request.message,
            response=response
        )
        db.add(new_history)
        db.commit()
        
        return AIResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[ChatHistoryResponse])
def get_history(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Get prompt history for the current user."""
    history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp.desc()).all()
    return history
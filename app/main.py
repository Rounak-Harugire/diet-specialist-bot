from fastapi import FastAPI, HTTPException
from app.chatbot import get_diet_chain
from app.database import get_chat_history
from app.schemas import ChatRequest

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    prompt_template, primary_llm, backup_llm = get_diet_chain()
    history_manager = get_chat_history(request.session_id)
    
    # Limit history to stay under token limits
    limited_history = history_manager.messages[-4:] 
    chain_input = {"input": request.message, "history": limited_history}

    try:
        # 1. Try Primary Model
        chain = prompt_template | primary_llm
        response = chain.invoke(chain_input)
    except Exception as e:
        print(f"Primary Model Failed: {e}")
        try:
            # 2. Try Backup Model if Primary fails
            chain = prompt_template | backup_llm
            response = chain.invoke(chain_input)
        except Exception as e_backup:
            # 3. If both fail, send specific error text to Frontend
            error_str = str(e_backup).lower()
            if "rate_limit" in error_str or "429" in error_str:
                return {"response": "RATE_LIMIT_ERROR"}
            return {"response": f"SYSTEM_ERROR: {str(e_backup)}"}

    # Save to DB if successful
    history_manager.add_user_message(request.message)
    history_manager.add_ai_message(response.content)
    return {"response": response.content}

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    history = get_chat_history(session_id)
    return {"history": [{"role": "user" if m.type=="human" else "assistant", "content": m.content} for m in history.messages]}
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

def get_diet_chain():
    # Primary Model (Higher quality)
    primary_llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=1024
    )
    
    # Backup Model (Faster, lower rate-limit risk)
    backup_llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=1024
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional Diet Specialist. Provide science-based advice."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    
    # We return the prompt and both LLMs so main.py can choose
    return prompt, primary_llm, backup_llm
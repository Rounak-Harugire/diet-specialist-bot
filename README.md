🥗 NutriMind AI - Diet Specialist Bot
A production-ready AI nutritionist powered by FastAPI, Streamlit, and LangChain. This bot provides personalized dietary advice using the Groq Llama 3 model and stores chat history in MongoDB Atlas.

🚀 Live Demo
Check out the live bot here! :- https://ai-diet-specialist-production.up.railway.app/

🛠️ Features
Intelligent Dietary Analysis:

Provides science-backed nutritional advice.

Tailors suggestions based on user-specific goals (weight loss, muscle gain, etc.).

Persistent Conversation Memory:

Integrates MongoDB Atlas to store and retrieve chat history.

Remembers user preferences across different sessions.

High-Performance API:

Built with FastAPI for asynchronous request handling.

Optimized for low-latency responses using Groq's Llama 3 hardware acceleration.

Modern Web Interface:

Developed with Streamlit for a responsive, user-friendly experience.

Features a clean "chat-bubble" UI with real-time feedback.

Production-Grade Security:

Implements environment variable protection for API keys.

Secured backend-to-database communication.

📦 Tech Stack
Language: Python 3.10+

LLM: Groq (Llama-3-70b-versatile)

Orchestration: LangChain

Backend: FastAPI (Uvicorn)

Frontend: Streamlit

Database: MongoDB Atlas (NoSQL)

Deployment: Railway.app

🏗️ Architecture
Frontend: Sends user queries to the FastAPI endpoint.

Backend: Processes logic, manages LangChain "memory" buffers, and fetches history from MongoDB.

AI Engine: Groq processes the prompt and returns a response in milliseconds.

Database: Every interaction is logged in a NoSQL document format for future retrieval.

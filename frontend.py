import streamlit as st
import requests
import uuid
import time
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NutriMind AI - Diet Assistant",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────
if "started" not in st.session_state:
    st.session_state.started = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "history_loaded" not in st.session_state:
    st.session_state.history_loaded = False
if "processing" not in st.session_state:
    st.session_state.processing = False

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
BACKEND_URL = "http://127.0.0.1:8000"

# ─────────────────────────────────────────────────────────────
# PREMIUM DARK THEME CSS WITH NEON ACCENTS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Clash+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* ─────────────────────────────────────────────────────────
       PREMIUM DARK THEME VARIABLES
       ───────────────────────────────────────────────────────── */
    :root {
        --bg-primary: #0A0A0F;
        --bg-secondary: #12121A;
        --bg-tertiary: #1A1A24;
        --bg-card: #1E1E2A;
        --text-primary: #FFFFFF;
        --text-secondary: #B8B8D0;
        --text-tertiary: #80809A;
        --neon-green: #00FF9D;
        --neon-purple: #B721FF;
        --neon-cyan: #00E0FF;
        --neon-pink: #FF3B7F;
        --neon-yellow: #FFD700;
        --accent-gradient: linear-gradient(135deg, #00FF9D, #00E0FF, #B721FF);
        --card-gradient: linear-gradient(145deg, rgba(30,30,42,0.9), rgba(20,20,30,0.95));
        --glow-green: 0 0 20px rgba(0, 255, 157, 0.3);
        --glow-purple: 0 0 20px rgba(183, 33, 255, 0.3);
        --glow-cyan: 0 0 20px rgba(0, 224, 255, 0.3);
        --border-glow: 0 0 2px rgba(0, 255, 157, 0.5);
        --shadow-soft: 0 8px 32px rgba(0, 0, 0, 0.4);
    }

    /* ─────────────────────────────────────────────────────────
       GLOBAL STYLES
       ───────────────────────────────────────────────────────── */
    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .main > .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        background: var(--bg-primary);
    }

    /* Hide Streamlit Branding */
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--neon-green);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--neon-cyan);
    }

    /* ─────────────────────────────────────────────────────────
       PREMIUM TOP BAR
       ───────────────────────────────────────────────────────── */
    .top-bar {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: rgba(10, 10, 15, 0.8);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(0, 255, 157, 0.2);
        padding: 16px 52px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }

    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .logo-mark {
        width: 44px;
        height: 44px;
        background: var(--accent-gradient);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: var(--bg-primary);
        box-shadow: var(--glow-green);
    }

    .logo-text {
        font-family: 'Clash Display', sans-serif;
        font-size: 24px;
        font-weight: 700;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .badge {
        background: var(--bg-tertiary);
        color: var(--neon-green);
        font-family: 'Space Grotesk', monospace;
        font-size: 12px;
        padding: 6px 16px;
        border-radius: 30px;
        border: 1px solid var(--neon-green);
        box-shadow: var(--glow-green);
        letter-spacing: 0.5px;
    }

    .live-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--text-secondary);
        font-size: 13px;
        font-family: 'Space Grotesk', monospace;
    }

    .live-dot {
        width: 10px;
        height: 10px;
        background: var(--neon-green);
        border-radius: 50%;
        box-shadow: var(--glow-green);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }

    /* ─────────────────────────────────────────────────────────
       HERO SECTION
       ───────────────────────────────────────────────────────── */
/* Hero Section */
.hero-section {
    padding: 80px 52px 60px;
    text-align: center;  /* This centers all inline content */
    background: var(--bg-primary);
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    right: -50%;
    bottom: -50%;
    background: radial-gradient(circle, rgba(0,255,157,0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

.hero-eyebrow {
    display: inline-block;  /* This makes it respect text-align: center */
    background: var(--bg-tertiary);
    padding: 8px 20px;
    border-radius: 40px;
    font-family: 'Space Grotesk', monospace;
    font-size: 13px;
    color: var(--neon-cyan);
    margin-bottom: 30px;
    border: 1px solid rgba(0, 224, 255, 0.3);
    box-shadow: var(--glow-cyan);
    position: relative;
    z-index: 2;
}

.hero-title {
    font-family: 'Clash Display', sans-serif;
    font-size: 96px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 24px;
    position: relative;
    z-index: 2;
    text-align: center;  /* Explicitly center */
}

.hero-gradient-text {
    background: linear-gradient(135deg, #00FF9D, #00E0FF, #B721FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 30px rgba(0,255,157,0.3);
}

.hero-subtitle {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
    max-width: 700px !important;
    width: 100% !important;
    padding: 0 20px !important;
    box-sizing: border-box !important;
}

    /* ─────────────────────────────────────────────────────────
       PREMIUM BUTTONS
       ───────────────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #00FF9D, #00E0FF) !important;
        color: var(--bg-primary) !important;
        font-family: 'Clash Display', sans-serif !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 16px 40px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.5) !important;
        transition: all 0.3s ease !important;
        width: auto !important;
        min-width: 280px !important;
        height: auto !important;
        letter-spacing: 1px !important;
        position: relative;
        z-index: 2;
        text-align: center !important;
    }

    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 0 40px rgba(0, 255, 157, 0.8) !important;
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }

    /* ─────────────────────────────────────────────────────────
       FEATURES SECTION
       ───────────────────────────────────────────────────────── */
    .features-section {
        padding: 80px 52px;
        background: var(--bg-secondary);
        position: relative;
    }

    .section-title {
        text-align: center;
        font-family: 'Clash Display', sans-serif;
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 60px;
        background: linear-gradient(135deg, #fff, #B8B8D0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
        max-width: 1200px;
        margin: 0 auto;
    }

    .feature-card {
        background: var(--bg-card);
        border-radius: 24px;
        padding: 40px 30px;
        text-align: center;
        border: 1px solid rgba(0, 255, 157, 0.1);
        box-shadow: var(--shadow-soft);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0,255,157,0.1), transparent);
        transition: left 0.5s ease;
    }

    .feature-card:hover::before {
        left: 100%;
    }

    .feature-card:hover {
        transform: translateY(-8px);
        border-color: var(--neon-green);
        box-shadow: var(--glow-green), var(--shadow-soft);
    }

    .feature-icon {
        font-size: 48px;
        margin-bottom: 20px;
        filter: drop-shadow(0 0 10px var(--neon-green));
    }

    .feature-title {
        font-family: 'Clash Display', sans-serif;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #fff, var(--neon-green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .feature-description {
        color: var(--text-secondary);
        line-height: 1.7;
        font-size: 15px;
    }

    /* ─────────────────────────────────────────────────────────
       CHAT INTERFACE - PREMIUM DARK THEME
       ───────────────────────────────────────────────────────── */
    .chat-top-bar {
        background: rgba(10, 10, 15, 0.9);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(0, 255, 157, 0.2);
        padding: 12px 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* User Message - Neon Style */
    [data-testid="stChatMessage"][aria-label="user"] [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #1A1A2A, #12121A) !important;
        border: 1px solid var(--neon-purple) !important;
        border-radius: 24px 24px 4px 24px !important;
        padding: 16px 24px !important;
        box-shadow: 0 0 30px rgba(183, 33, 255, 0.3) !important;
        margin-left: auto !important;
        max-width: 70% !important;
    }

    [data-testid="stChatMessage"][aria-label="user"] [data-testid="stChatMessageContent"] p {
        color: var(--text-primary) !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    /* Assistant Message - Premium Card */
    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--neon-green) !important;
        border-radius: 24px 24px 24px 4px !important;
        padding: 20px 28px !important;
        box-shadow: var(--glow-green), var(--shadow-soft) !important;
        max-width: 80% !important;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] p {
        color: var(--text-primary) !important;
        font-size: 16px !important;
        line-height: 1.7 !important;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] strong {
        color: var(--neon-green) !important;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] em {
        color: var(--neon-cyan) !important;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] ul,
    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] ol {
        color: var(--text-secondary) !important;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] li {
        color: var(--text-secondary) !important;
        margin-bottom: 6px !important;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] h1,
    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] h2,
    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] h3 {
        color: var(--neon-green) !important;
        font-family: 'Clash Display', sans-serif !important;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] code {
        background: var(--bg-secondary) !important;
        color: var(--neon-cyan) !important;
        padding: 2px 8px !important;
        border-radius: 8px !important;
        border: 1px solid rgba(0, 224, 255, 0.3) !important;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] [data-testid="stChatMessageContent"] blockquote {
        border-left: 3px solid var(--neon-purple) !important;
        background: rgba(183, 33, 255, 0.1) !important;
        padding: 12px 20px !important;
        border-radius: 0 16px 16px 0 !important;
        color: var(--text-secondary) !important;
    }

    /* Avatars */
    [data-testid="chatAvatarIcon-user"] > div {
        background: linear-gradient(135deg, #B721FF, #00E0FF) !important;
        color: var(--text-primary) !important;
        box-shadow: 0 0 20px rgba(183, 33, 255, 0.5) !important;
    }

    [data-testid="chatAvatarIcon-assistant"] > div {
        background: linear-gradient(135deg, #00FF9D, #00E0FF) !important;
        color: var(--bg-primary) !important;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.5) !important;
    }

    /* Chat Input - Premium Style */
    [data-testid="stChatInput"] {
        border: 2px solid transparent !important;
        border-radius: 50px !important;
        background: var(--bg-tertiary) !important;
        margin: 0 32px 24px 32px !important;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--neon-green) !important;
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.5) !important;
    }

    [data-testid="stChatInput"] textarea {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        padding: 16px 24px !important;
        background: transparent !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--text-tertiary) !important;
        font-weight: 300 !important;
    }

    [data-testid="stChatInputSubmitButton"] button {
        background: linear-gradient(135deg, #00FF9D, #00E0FF) !important;
        color: var(--bg-primary) !important;
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        margin-right: 8px !important;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.5) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stChatInputSubmitButton"] button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.8) !important;
    }

    /* Welcome Screen */
    .welcome-screen {
        text-align: center;
        padding: 60px 20px;
        background: var(--bg-primary);
    }

    .welcome-icon {
        font-size: 80px;
        margin-bottom: 24px;
        filter: drop-shadow(0 0 30px var(--neon-green));
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    .welcome-title {
        font-family: 'Clash Display', sans-serif;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #fff, var(--neon-green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .welcome-subtitle {
        color: var(--text-secondary);
        font-size: 18px;
        max-width: 600px;
        margin: 0 auto 48px;
    }

    /* Starter Questions */
    .starters-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        max-width: 700px;
        margin: 0 auto;
    }

    .starter-card {
        background: var(--bg-card);
        border: 1px solid rgba(0, 255, 157, 0.2);
        border-radius: 20px;
        padding: 20px;
        text-align: left;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-soft);
    }

    .starter-card:hover {
        border-color: var(--neon-green);
        transform: translateY(-4px);
        box-shadow: var(--glow-green), var(--shadow-soft);
    }

    .starter-icon {
        font-size: 28px;
        margin-bottom: 12px;
        filter: drop-shadow(0 0 10px var(--neon-green));
    }

    .starter-text {
        color: var(--text-primary);
        font-weight: 500;
        font-size: 15px;
    }

    /* Back Button */
    .back-button {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: 1px solid rgba(0, 255, 157, 0.3) !important;
        border-radius: 30px !important;
        padding: 8px 24px !important;
        font-size: 14px !important;
        min-width: auto !important;
        box-shadow: none !important;
    }

    .back-button:hover {
        background: var(--neon-green) !important;
        color: var(--bg-primary) !important;
        border-color: var(--neon-green) !important;
        box-shadow: var(--glow-green) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid rgba(0, 255, 157, 0.2) !important;
        padding: 24px !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary) !important;
    }

    /* Typing Indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 16px 24px;
        background: var(--bg-card);
        border-radius: 24px 24px 24px 4px;
        width: fit-content;
        border: 1px solid var(--neon-green);
        box-shadow: var(--glow-green);
        margin: 10px 0;
    }

    .typing-dot {
        width: 10px;
        height: 10px;
        background: var(--neon-green);
        border-radius: 50%;
        animation: bounce 1.4s infinite;
        box-shadow: var(--glow-green);
    }

    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }

    /* Footer */
    .footer {
        padding: 40px 52px;
        background: var(--bg-secondary);
        border-top: 1px solid rgba(0, 255, 157, 0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .footer-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Clash Display', sans-serif;
        font-size: 18px;
        color: var(--neon-green);
    }

    .footer-text {
        font-family: 'Space Grotesk', monospace;
        font-size: 13px;
        color: var(--text-tertiary);
    }

    /* Responsive */
    @media (max-width: 768px) {
        .hero-title { font-size: 48px; }
        .features-grid { grid-template-columns: 1fr; }
        .top-bar, .footer { padding: 16px 20px; }
        .hero-section, .features-section { padding: 40px 20px; }
        .starters-grid { grid-template-columns: 1fr; }
        [data-testid="stChatMessageContent"] { max-width: 90% !important; }
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def send_message_to_backend(message):
    """Send message to backend and return response"""
    try:
        payload = {
            "message": message,
            "session_id": st.session_state.session_id
        }
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return "🌟 I'm having trouble connecting. Please try again in a moment."
            
    except Exception:
        return "🔌 Connection error. Please ensure the backend server is running."

# ─────────────────────────────────────────────────────────────
# MAIN APP LOGIC
# ─────────────────────────────────────────────────────────────

if not st.session_state.started:
    # ─────────────────────────────────────────────────────────
    # PREMIUM LANDING PAGE
    # ─────────────────────────────────────────────────────────
    
    # Top Bar
    st.markdown("""
    <div class="top-bar">
        <div class="logo-container">
            <div class="logo-mark">🥑</div>
            <span class="logo-text">NutriMind AI</span>
        </div>
        <div style="display: flex; align-items: center; gap: 20px;">
            <span class="badge">⚡ PREMIUM AI</span>
            <span class="live-indicator">
                <span class="live-dot"></span>
                LIVE · 24/7 ONLINE
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-eyebrow">
            ⚡ Transform your health through the power of personalized AI nutrition
        </div>
        <h1 class="hero-title">
            Your Intelligent<br>
            <span class="hero-gradient-text">Nutrition Companion</span>
        </h1>
        <p class="hero-subtitle",style="text-align:center; margin-left:auto; margin-right:auto;">
            Experience the future of nutrition with AI-powered precision. 
            Get personalized meal plans, expert guidance, and science-backed advice 
            — all in one premium conversation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ START YOUR JOURNEY ✨", key="cta_main"):
            st.session_state.started = True
            st.rerun()

    # Features Section
    st.markdown("""
    <div class="features-section">
        <h2 class="section-title">Premium Features</h2>
        <div class="features-grid">
    """, unsafe_allow_html=True)

    features = [
        ("📋", "Custom Meal Plans", "AI-generated 7-day plans tailored to your goals, preferences, and dietary restrictions."),
        ("⚖️", "Precision Tracking", "Advanced macro calculations with real-time adjustments for optimal results."),
        ("🩺", "Medical Integration", "Evidence-based protocols for diabetes, PCOS, hypertension, and more."),
        ("💪", "Performance Optimization", "Sports nutrition strategies used by elite athletes and trainers."),
        ("🌱", "Lifestyle Adaptation", "Expert guidance for any diet: Vegan, Keto, Mediterranean, Paleo, and more."),
        ("📊", "Smart Analytics", "Track progress with AI-powered insights and personalized recommendations.")
    ]

    for icon, title, desc in features:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-description">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-logo">
            <span>🥑</span> NutriMind AI 
        </div>
        <span class="footer-text">GROQ · LLAMA 3.3 · FASTAPI</span>
        <span class="footer-text">© 2026 · SCIENCE-BASED NUTRITION</span>
    </div>
    """, unsafe_allow_html=True)

else:
    # ─────────────────────────────────────────────────────────
    # PREMIUM CHAT INTERFACE
    # ─────────────────────────────────────────────────────────
    
    # Chat Top Bar with Back Button
    col1, col2, col3 = st.columns([2, 6, 2])
    
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #00FF9D, #00E0FF); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px;">🥑</div>
            <span style="font-family: 'Clash Display', sans-serif; font-weight: 600; background: linear-gradient(135deg, #fff, #00FF9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">NutriMind</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; justify-content: center;">
            <span class="live-dot"></span>
            <span style="color: var(--text-secondary); font-family: 'Space Grotesk', monospace;">NutriMind AI ·  ACTIVE</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("← BACK", key="back_to_home", help="Return to home"):
            st.session_state.started = False
            st.session_state.messages = []
            st.rerun()

    # Main Chat Area
    chat_container = st.container()

    with chat_container:
        # Welcome Screen (if no messages)
        if not st.session_state.messages:
            st.markdown("""
            <div class="welcome-screen">
                <div class="welcome-icon">🥑</div>
                <h2 class="welcome-title">Welcome to NutriMind AI</h2>
                <p class="welcome-subtitle" style="text-align:center; margin-left:auto; margin-right:auto;">
                    Ask me anything about your diet, health goals, or nutritional needs. 
                    I'm here to provide expert, science-based guidance.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Starter Questions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎯 7-Day Premium Meal Plan", key="starter1", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Create a premium 7-day meal plan for weight loss with high protein"})
                    st.rerun()
                if st.button("💪 Muscle Building Protocol", key="starter3", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "What's the optimal protein intake and meal timing for muscle building?"})
                    st.rerun()
            
            with col2:
                if st.button("🩺 Blood Sugar Optimization", key="starter2", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Create a meal plan to stabilize blood sugar and manage insulin sensitivity"})
                    st.rerun()
                if st.button("🌱 Premium Vegan Athlete", key="starter4", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Design a high-energy vegan meal plan for athletic performance"})
                    st.rerun()

        # Display Chat History
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "🥑"):
                st.markdown(message["content"])

        # Handle Processing State
        if st.session_state.processing:
            st.markdown("""
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
            """, unsafe_allow_html=True)

    # Chat Input
    if prompt := st.chat_input(
        "Ask me about premium nutrition, meal planning, or health optimization...",
        disabled=st.session_state.processing
    ):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Set processing state
        st.session_state.processing = True
        st.rerun()

    # Process message
    if st.session_state.processing:
        with st.chat_message("assistant", avatar="🥑"):
            last_message = st.session_state.messages[-1]["content"]
            response = send_message_to_backend(last_message)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.session_state.processing = False
        st.rerun()

    # Premium Sidebar
    with st.sidebar:
        st.markdown("### ⚡ PREMIUM CONTROLS")
        st.markdown("---")
        
        st.markdown("**Session ID**")
        st.code(st.session_state.session_id[:12], language="text")
        
        if st.button("🗑️ CLEAR CONVERSATION", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        with st.expander("💡 PREMIUM TIPS", expanded=True):
            st.markdown("""
            • Ask about **personalized meal plans**
            • Request **macro optimization**
            • Get **condition-specific advice**
            • Learn **timing strategies**
            • Discover **food combinations**
            """)
        
        with st.expander("⚕️ MEDICAL DISCLAIMER"):
            st.markdown("""
            This AI provides educational information only. 
            Always consult with healthcare providers for medical decisions.
            """)
        
        st.markdown("---")
        st.markdown("**✨ PREMIUM FEATURES**")
        st.markdown("• Real-time analysis")
        st.markdown("• Personalized protocols")
        st.markdown("• Science-backed data")
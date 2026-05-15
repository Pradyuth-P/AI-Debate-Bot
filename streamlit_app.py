import streamlit as st
import os
import json
import uuid
import re
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict
from groq import AsyncGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Models & Schemas ---

class DebateSide(str, Enum):
    FOR = "FOR"
    AGAINST = "AGAINST"

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class ConversationMessage:
    role: str
    content: str

@dataclass
class ArgumentAnalysis:
    strength: str
    key_points: List[str]
    logical_fallacies: Optional[List[str]] = None
    rating: int = 5

# --- Prompts ---

class DebatePrompts:
    @staticmethod
    def get_system_prompt(topic: str, side: DebateSide) -> str:
        side_instruction = "strongly in FAVOR of" if side == DebateSide.FOR else "strongly AGAINST"
        opposing_view = "against" if side == DebateSide.FOR else "in favor of"
        return f"""You are an elite debate champion and expert argumentation specialist.
DEBATE CONFIGURATION:
- Topic: "{topic}"
- Your Position: You are arguing {side_instruction} this topic
- The human is arguing {opposing_view} this topic

YOUR DEBATE PERSONA:
- Intellectually confident, sharp, and persuasive.
- Use evidence, logic, and rhetorical techniques masterfully.
- Never concede your main position.
- End responses with a thought-provoking challenge or question.
- Keep responses focused (150-250 words).

TONE: Intellectually fierce, confident, eloquent, and engaging."""

    @staticmethod
    def get_opening_prompt(topic: str, side: DebateSide) -> str:
        position = "FOR" if side == DebateSide.FOR else "AGAINST"
        return f"""Deliver a powerful opening argument for the debate topic: "{topic}"
You are arguing {position} this proposition.
1. Start with a compelling hook.
2. Clearly state your position.
3. Present 2-3 strongest arguments.
4. End with a challenge.
Keep it to 200-280 words."""

    @staticmethod
    def get_counter_argument_prompt(user_argument: str, turn_number: int) -> str:
        intensity = "escalating intensity" if turn_number > 3 else "measured confidence"
        return f"""The opponent has made this argument (Turn {turn_number}):
"{user_argument}"
Respond with {intensity}.
1. Dismantle their weakest point.
2. Present a powerful counter-point.
3. Use statistics/examples/logic.
4. End with a sharp question.
150-250 words."""

    @staticmethod
    def get_analysis_prompt(user_argument: str) -> str:
        return f"""Analyze this debate argument objectively and return a JSON response:
Argument: "{user_argument}"
Return ONLY valid JSON:
{{
  "strength": "1-sentence assessment",
  "key_points": ["point 1", "point 2"],
  "logical_fallacies": ["fallacy name" or null],
  "rating": <int 1-10>
}}"""

# --- Utilities ---

def run_async(coro):
    """Run an async coroutine in a way that works with Streamlit's event loop."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

# --- Services ---

class LLMService:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        if not self.groq_key:
            # Fallback to secrets if on Streamlit Cloud
            try:
                self.groq_key = st.secrets["GROQ_API_KEY"]
            except:
                pass
                
        self.groq_client = AsyncGroq(api_key=self.groq_key) if self.groq_key else None
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        if not self.groq_client:
            raise RuntimeError("GROQ_API_KEY is not set in environment or secrets.")
            
        try:
            response = await self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=messages,
                temperature=0.8,
                max_tokens=1000,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Groq API error: {str(e)}")

    async def json_completion(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        if not self.groq_client:
            return {
                "strength": "Groq not configured",
                "key_points": ["Analysis failed"],
                "logical_fallacies": None,
                "rating": 5
            }

        content = ""
        try:
            response = await self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=messages,
                temperature=0.3,
            )
            content = response.choices[0].message.content.strip()
            
            # Cleanup content for JSON parsing
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
        except Exception as e:
            if content:
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group())
                    except: pass
            return {
                "strength": "Analysis unavailable",
                "key_points": ["Analysis failed"],
                "logical_fallacies": None,
                "rating": 5
            }

# --- Streamlit UI ---

st.set_page_config(
    page_title="DEBATE.AI | The Future of Argumentation",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Premium UI CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    :root {
        --primary: #8B5CF6;
        --primary-glow: rgba(139, 92, 246, 0.4);
        --secondary: #EC4899;
        --bg-dark: #05050A;
        --card-bg: rgba(17, 17, 27, 0.7);
        --text-main: #E2E8F0;
        --text-muted: #94A3B8;
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(139, 92, 246, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(236, 72, 153, 0.05) 0%, transparent 40%);
        color: var(--text-main);
    }
    
    /* Animation for glass cards */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 24px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
        animation: fadeIn 0.6s ease-out;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #A78BFA 0%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.03em;
    }
    
    /* AI Message Bubble */
    .ai-bubble {
        background: linear-gradient(165deg, rgba(30, 30, 50, 0.6), rgba(15, 15, 25, 0.6));
        border: 1px solid rgba(139, 92, 246, 0.2);
        padding: 1.5rem;
        border-radius: 4px 24px 24px 24px;
        margin: 2rem 0;
        font-size: 1.1rem;
        line-height: 1.7;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* User Message Bubble */
    .user-bubble {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(236, 72, 153, 0.2);
        padding: 1.5rem;
        border-radius: 24px 4px 24px 24px;
        margin: 2rem 0;
        text-align: right;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    
    .rating-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1.25rem;
        border-radius: 12px;
        background: rgba(139, 92, 246, 0.15);
        color: #C4B5FD;
        font-weight: 600;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }

    /* Better looking buttons */
    .stButton>button {
        background: linear-gradient(90deg, #7C3AED, #DB2777);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px var(--primary-glow);
    }

    /* Sidebar customization */
    section[data-testid="stSidebar"] {
        background-color: #030307;
        border-right: 1px solid rgba(255, 255, 255, 0.03);
    }

    .sidebar-title {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }

    /* Input focus effect */
    .stTextArea textarea {
        background: rgba(10, 10, 20, 0.6) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #fff !important;
        padding: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px var(--primary-glow) !important;
    }

    /* Hide standard Streamlit header/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "debate_active" not in st.session_state:
    st.session_state.debate_active = False
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "side" not in st.session_state:
    st.session_state.side = DebateSide.FOR
if "turn_number" not in st.session_state:
    st.session_state.turn_number = 0
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = ""

# Services
llm = LLMService()

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='gradient-text sidebar-title'>DEBATE.AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 0.95rem; margin-top: -10px;'>Advanced Intelligence Dual.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### ⚙️ DEBATE ENGINE")
    st.markdown("<div style='background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    st.write(f"**Provider:** `Groq`")
    st.write(f"**Model:** `Llama-3.3-70b`")
    st.write(f"**Status:** {'🟢 Ready' if llm.groq_client else '🔴 API Key Missing'}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏛️ DEBATE SETUP")
    
    if not st.session_state.debate_active:
        topic_input = st.text_area("Debate Topic", placeholder="Enter a controversial topic...", height=150)
        side_input = st.radio("AI's Position", ["FOR", "AGAINST"], horizontal=True)
        
        if st.button("INITIATE DUAL"):
            if not llm.groq_client:
                st.error("GROQ_API_KEY is not configured in the environment.")
            elif len(topic_input) < 5:
                st.warning("Topic is too short for a rigorous debate.")
            else:
                with st.spinner("Analyzing topic and preparing opening argument..."):
                    st.session_state.topic = topic_input
                    st.session_state.side = DebateSide(side_input)
                    st.session_state.debate_active = True
                    st.session_state.turn_number = 0
                    st.session_state.messages = []
                    st.session_state.system_prompt = DebatePrompts.get_system_prompt(topic_input, st.session_state.side)
                    
                    opening_prompt = DebatePrompts.get_opening_prompt(topic_input, st.session_state.side)
                    msgs = [
                        {"role": "system", "content": st.session_state.system_prompt},
                        {"role": "user", "content": opening_prompt}
                    ]
                    try:
                        response = run_async(llm.chat_completion(msgs))
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.session_state.turn_number += 1
                        st.rerun()
                    except Exception as e:
                        st.error(f"Initialization Failed: {str(e)}")
                        st.session_state.debate_active = False
    else:
        st.markdown(f"**Exchanges:** `{st.session_state.turn_number}`")
        st.markdown(f"**AI Side:** `{st.session_state.side.value}`")
        
        if st.button("TERMINATE"):
            st.session_state.debate_active = False
            st.session_state.messages = []
            st.session_state.last_analysis = None
            st.rerun()

# Main Interface
if not st.session_state.debate_active:
    st.markdown("<div style='text-align: center; padding-top: 80px; max-width: 800px; margin: 0 auto;'>", unsafe_allow_html=True)
    st.markdown("<h1 class='gradient-text' style='font-size: 5rem; margin-bottom: 0;'>The Arena.</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #E2E8F0; font-size: 2rem; font-weight: 300; margin-top: 0;'>Challenge pure logic.</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.2rem; line-height: 1.6; margin-top: 30px;'>Engage in a sophisticated intellectual duel with an AI trained in the arts of rhetoric and philosophy. Configure your debate in the sidebar to begin.</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #A78BFA; margin-top: 0;'>🧠 Neural Logic</h4>
            <p style='font-size: 0.9rem; color: #94A3B8;'>Powered by ultra-fast Llama-3 inference on Groq hardware.</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #F472B6; margin-top: 0;'>📊 Analytics</h4>
            <p style='font-size: 0.9rem; color: #94A3B8;'>Get objective ratings and fallacy detection for every argument you make.</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #60A5FA; margin-top: 0;'>🛡️ Integrity</h4>
            <p style='font-size: 0.9rem; color: #94A3B8;'>Unwavering, context-aware debating that pushes your boundaries.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Header Area
    st.markdown(f"<div style='border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 1rem; margin-bottom: 2rem;'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 2.5rem; margin-bottom: 0;'>{st.session_state.topic}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #94A3B8; font-size: 1.1rem;'>AI is arguing <span style='color: #C4B5FD; font-weight: bold;'>{st.session_state.side.value}</span> the topic</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Message History
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class='ai-bubble'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;'>
                    <span style='color: #8B5CF6; font-weight: 700; font-size: 0.9rem; letter-spacing: 0.05em;'>AI DEBATER</span>
                </div>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='user-bubble'>
                <div style='margin-bottom: 0.8rem;'>
                    <span style='color: #EC4899; font-weight: 700; font-size: 0.9rem; letter-spacing: 0.05em;'>YOU (OPPONENT)</span>
                </div>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

    # Analytics Panel (Floating Style)
    if st.session_state.last_analysis:
        st.markdown("<div class='glass-card' style='border-left: 4px solid #DB2777;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top: 0;'>📊 JUDGE'S SCORECARD</h3>", unsafe_allow_html=True)
        
        analysis = st.session_state.last_analysis
        col1, col2 = st.columns([1, 2])
        
        with col1:
            rating = analysis.get('rating', 5)
            st.markdown(f"<div class='rating-badge'>Logic Score: {rating}/10</div>", unsafe_allow_html=True)
            st.progress(rating / 10)
            
        with col2:
            st.markdown(f"**Assessment:** {analysis.get('strength', 'N/A')}")
            
            fallacies = analysis.get('logical_fallacies')
            if fallacies and isinstance(fallacies, list) and fallacies[0]:
                st.markdown(f"**Fallacies:** <span style='color: #F87171;'>{', '.join(fallacies)}</span>", unsafe_allow_html=True)
            
            points = analysis.get('key_points', [])
            if points:
                st.markdown(f"**Extracted Points:** {', '.join(points)}")
                
        st.markdown("</div>", unsafe_allow_html=True)

    # Input Dock
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        with st.form("input_form", clear_on_submit=True):
            user_input = st.text_area("", placeholder="Deliver your counter-argument...", height=120, label_visibility="collapsed")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button("DELIVER ARGUMENT")
                
            if submitted and user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                async def process_turn():
                    # 1. Analyze
                    analysis_msgs = [
                        {"role": "system", "content": "You are a professional debate judge. Analyze and return JSON."},
                        {"role": "user", "content": DebatePrompts.get_analysis_prompt(user_input)}
                    ]
                    st.session_state.last_analysis = await llm.json_completion(analysis_msgs)
                    
                    # 2. Respond
                    debate_msgs = [{"role": "system", "content": st.session_state.system_prompt}]
                    for m in st.session_state.messages:
                        debate_msgs.append(m)
                    
                    counter_prompt = DebatePrompts.get_counter_argument_prompt(user_input, st.session_state.turn_number)
                    debate_msgs.append({"role": "user", "content": counter_prompt})
                    
                    response = await llm.chat_completion(debate_msgs)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.turn_number += 1

                with st.spinner("AI is formulating a rebuttal..."):
                    try:
                        run_async(process_turn())
                        st.rerun()
                    except Exception as e:
                        st.error(f"Critical Error: {str(e)}")

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #475569; font-size: 0.85rem; padding: 2rem; border-top: 1px solid rgba(255,255,255,0.03);'>", unsafe_allow_html=True)
st.write("DEBATE.AI v1.2 | High-Fidelity Argumentation Engine | Developed with Streamlit & Groq")
st.markdown("</div>", unsafe_allow_html=True)

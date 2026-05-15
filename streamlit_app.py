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
    def __init__(self, groq_key: str = None):
        self.groq_key = groq_key or os.getenv("GROQ_API_KEY")
        self.groq_client = AsyncGroq(api_key=self.groq_key) if self.groq_key else None
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        if not self.groq_client:
            raise RuntimeError("Groq API Key is not configured.")
            
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
    page_title="AI Debate Bot | Powered by Groq",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    
    .stApp {
        background-color: #0A0A0F;
        color: #E2E8F0;
    }
    
    .glass-card {
        background: rgba(26, 26, 36, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(129, 140, 248, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .ai-bubble {
        background: linear-gradient(145deg, rgba(30, 30, 50, 0.8), rgba(20, 20, 40, 0.8));
        border-left: 4px solid #818CF8;
        padding: 1.25rem;
        border-radius: 4px 16px 16px 4px;
        margin: 1.5rem 0;
        font-size: 1.05rem;
        line-height: 1.6;
        border: 1px solid rgba(129, 140, 248, 0.1);
    }
    
    .user-bubble {
        background: rgba(129, 140, 248, 0.05);
        border-right: 4px solid #C084FC;
        padding: 1.25rem;
        border-radius: 16px 4px 4px 16px;
        margin: 1.5rem 0;
        text-align: right;
        font-size: 1.05rem;
        line-height: 1.6;
        border: 1px solid rgba(192, 132, 252, 0.1);
    }
    
    .rating-badge {
        display: inline-block;
        padding: 0.35rem 1rem;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(129, 140, 248, 0.2), rgba(192, 132, 252, 0.2));
        color: #A5B4FC;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid rgba(129, 140, 248, 0.3);
    }

    .stButton>button {
        background: linear-gradient(90deg, #6366F1, #A855F7);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }

    .stTextArea>div>div>textarea {
        background: rgba(15, 15, 25, 0.8);
        color: #E2E8F0;
        border: 1px solid rgba(129, 140, 248, 0.2);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #05050A;
        border-right: 1px solid rgba(129, 140, 248, 0.1);
    }
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

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='gradient-text'>⚖️ DEBATE.AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>The ultimate AI sparring partner.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("🔑 API Configuration")
    groq_key = st.text_input("Groq API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")
    llm = LLMService(groq_key=groq_key)
    
    st.markdown("---")
    st.subheader("🛠️ Debate Setup")
    if not st.session_state.debate_active:
        topic_input = st.text_area("Debate Topic", placeholder="e.g., Space exploration is a waste of resources...", height=120)
        side_input = st.radio("AI's Position", ["FOR", "AGAINST"], horizontal=True)
        
        if st.button("🚀 INITIATE DEBATE", use_container_width=True):
            if not groq_key:
                st.error("Please provide a Groq API key!")
            elif len(topic_input) < 5:
                st.error("Topic is too short! Be more specific.")
            else:
                with st.spinner("Preparing arguments..."):
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
                        st.error(f"Failed to start debate: {str(e)}")
                        st.session_state.debate_active = False
    else:
        st.markdown(f"**Current Topic:**\n*{st.session_state.topic}*")
        st.markdown(f"**AI Position:** `{st.session_state.side.value}`")
        st.markdown(f"**Exchanges:** `{st.session_state.turn_number}`")
        
        if st.button("⏹️ TERMINATE DEBATE", use_container_width=True):
            st.session_state.debate_active = False
            st.session_state.messages = []
            st.session_state.last_analysis = None
            st.rerun()

# Main Interface
if not st.session_state.debate_active:
    st.markdown("<div style='text-align: center; padding-top: 100px;'>", unsafe_allow_html=True)
    st.markdown("<h2 class='gradient-text' style='font-size: 4rem; margin-bottom: 0;'>Master the Art.</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #E2E8F0; font-size: 1.5rem; font-weight: 400;'>Win the Argument.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; max-width: 600px; margin: 20px auto;'>Challenge state-of-the-art AI in a rigorous intellectual duel. Powered exclusively by Groq for lightning-fast responses.</p>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("<div class='glass-card'><h4>🧠 Groq Logic</h4><p style='font-size: 0.9rem;'>Powered by Llama-3 for peak reasoning and speed.</p></div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown("<div class='glass-card'><h4>📊 Analysis</h4><p style='font-size: 0.9rem;'>Real-time feedback on your argument strength.</p></div>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown("<div class='glass-card'><h4>🎭 Persona</h4><p style='font-size: 0.9rem;'>Unwavering AI positions to test your mettle.</p></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Topic Header
    st.markdown(f"<h2 style='margin-bottom: 0;'>{st.session_state.topic}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #94A3B8;'>AI is arguing {st.session_state.side.value}</p>", unsafe_allow_html=True)
    
    # Chat History
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class='ai-bubble'>
                <small style='color: #818CF8; font-weight: bold;'>DEBATE BOT ({st.session_state.side.value})</small><br>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='user-bubble'>
                <small style='color: #C084FC; font-weight: bold;'>YOU (OPPOSING)</small><br>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

    # Latest Analysis
    if st.session_state.last_analysis:
        with st.container():
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("📊 Argument Analytics")
            analysis = st.session_state.last_analysis
            col1, col2 = st.columns([1, 2])
            with col1:
                rating = analysis.get('rating', 5)
                st.markdown(f"<div class='rating-badge'>Strength Rating: {rating}/10</div>", unsafe_allow_html=True)
                st.progress(rating / 10)
            with col2:
                st.markdown(f"**Assessment:** {analysis.get('strength', 'N/A')}")
                if analysis.get('logical_fallacies'):
                    fallacies = analysis['logical_fallacies']
                    if isinstance(fallacies, list):
                        st.markdown(f"**Fallacies Detected:** <span style='color: #F87171;'>{', '.join([f for f in fallacies if f])}</span>", unsafe_allow_html=True)
                
                points = analysis.get('key_points', [])
                if points:
                    st.markdown(f"**Key Points Identified:** {', '.join(points)}")
            st.markdown("</div>", unsafe_allow_html=True)

    # Input Area
    st.markdown("---")
    with st.form("argument_form", clear_on_submit=True):
        user_input = st.text_area("Your Counter-Argument", placeholder="Deliver your counter-strike...", height=120)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button("🔥 SEND ARGUMENT", use_container_width=True)

        if submit_button and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            async def process_turn():
                # 1. Analyze user argument
                analysis_msgs = [
                    {"role": "system", "content": "You are an expert debate judge and argumentation analyst. Analyze the user's argument objectively and return JSON only."},
                    {"role": "user", "content": DebatePrompts.get_analysis_prompt(user_input)}
                ]
                analysis = await llm.json_completion(analysis_msgs)
                st.session_state.last_analysis = analysis
                
                # 2. Generate AI counter-argument
                debate_msgs = [{"role": "system", "content": st.session_state.system_prompt}]
                for m in st.session_state.messages:
                    debate_msgs.append(m)
                
                counter_prompt = DebatePrompts.get_counter_argument_prompt(user_input, st.session_state.turn_number)
                debate_msgs.append({"role": "user", "content": counter_prompt})
                
                response = await llm.chat_completion(debate_msgs)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.turn_number += 1

            with st.spinner("AI is analyzing and preparing a counter-strike..."):
                try:
                    run_async(process_turn())
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing turn: {str(e)}")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #4B5563; font-size: 0.8rem; padding: 2rem;'>DEBATE.AI v1.1 | Powered by Groq</div>", unsafe_allow_html=True)

# 🎤 AI Debate Bot (Streamlit Edition)

A high-fidelity, single-file AI debate application built with Streamlit. This version migrates the original React+FastAPI architecture into a streamlined, production-ready Python application with enhanced features and premium aesthetics.

---

## ✨ New Features in Streamlit Edition

| Feature | Description |
|---|---|
| 🚀 Single-File Deployment | No more managing separate frontend and backend services. |
| 🛡️ Groq-Native Engine | Optimized exclusively for **Groq** for lightning-fast debates. |
| ⚡ Sub-Second Responses | Leverages Llama-3 on Groq for near-instant counter-arguments. |
| 🎨 Premium UI | Custom CSS glassmorphism, gradients, and a sleek dark mode design. |
| 📊 Real-time Analytics | Deep analysis of user arguments including strength ratings and logical fallacies. |
| 🔑 In-App Configuration | Manage your Groq API key directly from the sidebar. |

---

## 🏗️ Architecture

The entire application logic is now consolidated into `streamlit_app.py`, making it extremely easy to deploy to platforms like Streamlit Community Cloud, Hugging Face Spaces, or any VPS.

```
ai-debate-bot/
├── streamlit_app.py          # Unified application (Logic + UI)
├── requirements.txt          # Minimal dependencies for Streamlit
├── .env.example              # Updated with Groq focus
└── README-STREAMLIT.md       # This guide
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory (or copy from `.env.example`):

```bash
cp .env.example .env
```

Add your Groq API key:
```env
GROQ_API_KEY=gsk-...
```

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`.

---

## ⚙️ Configuration

The app supports two main LLM providers:
- **OpenAI**: Defaults to `gpt-4o-mini`.
- **Groq**: Defaults to `llama-3.3-70b-versatile` (extremely fast).

You can switch between them in the sidebar at any time during a session.

---

## 🧪 Self-Debugging & Reliability

- **Async Support**: Uses a robust `run_async` utility to handle concurrent LLM calls and UI updates within Streamlit.
- **JSON Parsing**: Implements a multi-layered JSON extraction logic (Regex + Cleaning) to handle LLM responses that may be incorrectly formatted.
- **Provider Redundancy**: The `LLMService` is designed to automatically attempt a fallback if the primary provider encounters an error.

---

## 🎨 Design Philosophy

The Streamlit edition focuses on **Rich Aesthetics**:
- **Typography**: Uses 'DM Sans' for a modern, tech-forward look.
- **Gradients**: Vibrant linear gradients for branding and emphasis.
- **Layout**: Clean sidebar for configuration and a focused main area for the debate duel.
- **Micro-animations**: Smooth transitions and progress bars for argument ratings.

---

## 📄 License

MIT License — converted and enhanced by Antigravity AI.

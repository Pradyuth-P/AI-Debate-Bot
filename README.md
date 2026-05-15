# 🎤 AI Debate Bot

A production-ready full-stack AI debate application where users engage in real-time intellectual debates with a GPT-powered AI debater. The AI argues FOR or AGAINST any topic with sophisticated rhetoric, counter-arguments, and real-time argument analysis.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 Topic Selection | Enter any debate topic |
| ⚔️ Side Selection | AI argues FOR or AGAINST |
| 🤖 AI Counter-Arguments | Intelligent, context-aware rebuttals |
| 📊 Argument Analysis | Real-time rating (1-10), key points, logical fallacies |
| 🧠 Conversation Memory | Full session context maintained |
| 💬 ChatGPT-style UI | Dark, modern chat interface |
| ⌨️ Typing Indicators | Animated dots while AI responds |
| 📜 Chat History | Fully scrollable with auto-scroll |
| ⚡ Loading States | Visual feedback during API calls |
| 🛡️ Error Handling | Graceful error recovery |
| 📱 Responsive Design | Works on mobile and desktop |
| 🐳 Docker Ready | One-command deployment |

---

## 🏗️ Architecture

```
ai-debate-bot/
├── backend/                    # Python FastAPI
│   ├── main.py                 # FastAPI app entry point
│   ├── routes/
│   │   ├── debate.py           # Debate API endpoints
│   │   └── health.py           # Health check endpoint
│   ├── services/
│   │   ├── openai_service.py   # OpenAI API integration
│   │   ├── memory_service.py   # Session/conversation memory
│   │   └── debate_engine.py    # Core debate orchestration
│   ├── models/
│   │   └── schemas.py          # Pydantic data models
│   ├── prompts/
│   │   └── debate_prompts.py   # Centralized prompt management
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # React + Vite + TailwindCSS
│   ├── src/
│   │   ├── App.jsx             # Root component
│   │   ├── main.jsx            # React entry point
│   │   ├── index.css           # Global styles
│   │   ├── components/
│   │   │   ├── TopicSetup.jsx  # Debate configuration screen
│   │   │   ├── ChatInterface.jsx # Main chat container
│   │   │   ├── ChatHeader.jsx  # Debate info header
│   │   │   ├── MessageBubble.jsx # Individual message component
│   │   │   ├── TypingIndicator.jsx # AI typing animation
│   │   │   ├── ChatInput.jsx   # Message input bar
│   │   │   └── ErrorBanner.jsx # Error display
│   │   ├── hooks/
│   │   │   ├── useDebate.js    # Main state management hook
│   │   │   └── useAutoScroll.js # Auto-scroll hook
│   │   └── services/
│   │       └── debateApi.js    # Axios API client
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env.example
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **OpenAI API Key** — get one at [platform.openai.com](https://platform.openai.com)

---

### Option 1: Local Development (Recommended)

#### 1. Clone and setup environment

```bash
git clone <your-repo>
cd ai-debate-bot

# Copy and configure backend environment
cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENAI_API_KEY
```

#### 2. Start the Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload --port 8000
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

#### 3. Start the Frontend

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

### Option 2: Docker (Production)

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env and add OPENAI_API_KEY

# 2. Build and launch
docker-compose up --build

# App runs at http://localhost:80
# API at http://localhost:8000
```

---

## 🔌 API Reference

### POST `/api/debate/start`
Start a new debate session.

**Request:**
```json
{
  "topic": "AI will replace most human jobs within 20 years",
  "side": "FOR"
}
```

**Response:**
```json
{
  "session_id": "3f2a1b4c-...",
  "topic": "AI will replace most human jobs within 20 years",
  "side": "FOR",
  "opening_argument": "Let me begin with an undeniable truth...",
  "message": "Debate session started successfully"
}
```

---

### POST `/api/debate/message`
Send a user argument, receive AI counter-argument + analysis.

**Request:**
```json
{
  "session_id": "3f2a1b4c-...",
  "user_argument": "AI lacks the creativity and emotional intelligence to replace human workers"
}
```

**Response:**
```json
{
  "session_id": "3f2a1b4c-...",
  "counter_argument": "A fascinating claim, yet one that collapses under scrutiny...",
  "analysis": {
    "strength": "Moderately valid point that conflates creativity with task completion",
    "key_points": [
      "References emotional intelligence as a defense",
      "Assumes creativity is uniquely human",
      "Does not address economic displacement evidence"
    ],
    "logical_fallacies": ["Appeal to nature fallacy"],
    "rating": 6
  },
  "turn_number": 2,
  "topic": "AI will replace most human jobs within 20 years",
  "side": "FOR"
}
```

---

### GET `/api/debate/session/{session_id}`
Get debate summary and full conversation history.

---

### DELETE `/api/debate/session/{session_id}`
End and clean up a debate session.

---

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Debate Bot API",
  "version": "1.0.0",
  "openai_configured": true,
  "active_sessions": 3
}
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | (required) | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model to use |
| `MAX_TOKENS` | `1000` | Max tokens per response |
| `TEMPERATURE` | `0.8` | Generation creativity (0-1) |
| `SESSION_TTL_HOURS` | `2` | Session expiration time |

**Model options:**
- `gpt-4o-mini` — Fast and affordable, great for debates
- `gpt-4o` — Most capable, best arguments
- `gpt-4-turbo` — Powerful with large context

---

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Start a debate
curl -X POST http://localhost:8000/api/debate/start \
  -H "Content-Type: application/json" \
  -d '{"topic": "Remote work is more productive", "side": "FOR"}'

# Send an argument (replace SESSION_ID)
curl -X POST http://localhost:8000/api/debate/message \
  -H "Content-Type: application/json" \
  -d '{"session_id": "SESSION_ID", "user_argument": "Workers are more distracted at home"}'
```

---

## 🎨 UI Screenshots

The application features:
- **Dark theme** with dramatic debate aesthetics
- **Playfair Display** font for editorial gravitas  
- **Color-coded sides**: Green (FOR) vs Red (AGAINST)
- **Argument analysis panel** with animated rating bars
- **Typing animation** with bouncing dots
- **Glass morphism** cards with noise texture overlay

---

## 📦 Deployment

### Environment Variables for Production

```bash
# Backend
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
MAX_TOKENS=1200
TEMPERATURE=0.8

# Frontend (set at build time)
VITE_API_URL=https://your-backend-domain.com/api
```

### Docker Production Build

```bash
docker-compose -f docker-compose.yml up --build -d
```

### Manual Production

```bash
# Backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend
npm run build
# Serve dist/ with nginx or any static host
```

---

## 🔒 Security Notes

- Never commit `.env` files
- API key is stored server-side only — never exposed to the browser
- CORS is configured to restrict origins in production
- Session data is in-memory (no database required)
- Non-root Docker user for container security

---

## 📄 License

MIT License — feel free to use and modify.

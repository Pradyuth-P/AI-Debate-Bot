from models.schemas import (
    DebateSide,
    StartDebateResponse,
    DebateMessageResponse,
    ArgumentAnalysis,
    SessionSummaryResponse,
)
from services.openai_service import OpenAIService
from services.memory_service import MemoryService, DebateSession
from prompts.debate_prompts import DebatePrompts


class DebateEngine:
    """Core debate engine that orchestrates AI debate interactions."""

    def __init__(self, openai_service: OpenAIService, memory_service: MemoryService):
        self.openai = openai_service
        self.memory = memory_service
        self.prompts = DebatePrompts()

    async def start_debate(
        self, topic: str, side: DebateSide
    ) -> StartDebateResponse:
        """Initialize a new debate session and generate opening argument."""

        # Create system prompt for this debate configuration
        system_prompt = self.prompts.get_system_prompt(topic, side)

        # Create a new session in memory
        session = self.memory.create_session(topic, side, system_prompt)

        # Generate opening argument
        opening_prompt = self.prompts.get_opening_prompt(topic, side)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": opening_prompt},
        ]

        opening_argument = await self.openai.chat_completion(messages)

        # Store the opening argument in session memory
        session.add_message("assistant", opening_argument)
        session.increment_turn()

        return StartDebateResponse(
            session_id=session.session_id,
            topic=topic,
            side=side,
            opening_argument=opening_argument,
        )

    async def process_argument(
        self, session_id: str, user_argument: str
    ) -> DebateMessageResponse:
        """Process a user argument and generate counter-argument with analysis."""

        # Retrieve session from memory
        session = self.memory.get_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found or has expired")

        # Add user's argument to session memory
        session.add_message("user", user_argument)

        # Run analysis and counter-argument in parallel concepts
        # (sequential for simplicity, but structured for easy async upgrade)
        analysis = await self._analyze_argument(user_argument)
        counter_argument = await self._generate_counter_argument(session, user_argument)

        # Store AI response in memory
        session.add_message("assistant", counter_argument)
        session.increment_turn()

        return DebateMessageResponse(
            session_id=session_id,
            counter_argument=counter_argument,
            analysis=analysis,
            turn_number=session.turn_number,
            topic=session.topic,
            side=session.side,
        )

    async def _analyze_argument(self, user_argument: str) -> ArgumentAnalysis:
        """Analyze the strength and quality of a user's argument."""
        analysis_prompt = self.prompts.get_analysis_prompt(user_argument)
        messages = [
            {
                "role": "system",
                "content": "You are an expert debate judge and argumentation analyst. Analyze arguments objectively and return valid JSON only.",
            },
            {"role": "user", "content": analysis_prompt},
        ]

        try:
            analysis_data = await self.openai.json_completion(messages)
            # Ensure rating is within bounds
            rating = max(1, min(10, int(analysis_data.get("rating", 5))))
            fallacies = analysis_data.get("logical_fallacies", [])
            if fallacies and fallacies[0] == "null":
                fallacies = None

            return ArgumentAnalysis(
                strength=analysis_data.get("strength", "Moderate argument"),
                key_points=analysis_data.get("key_points", ["Point identified"])[:3],
                logical_fallacies=fallacies if fallacies else None,
                rating=rating,
            )
        except Exception:
            # Graceful fallback if analysis fails
            return ArgumentAnalysis(
                strength="Argument received and processed",
                key_points=["Argument noted", "Counter-argument prepared"],
                logical_fallacies=None,
                rating=5,
            )

    async def _generate_counter_argument(
        self, session: DebateSession, user_argument: str
    ) -> str:
        """Generate a counter-argument using full conversation context."""
        counter_prompt = self.prompts.get_counter_argument_prompt(
            user_argument, session.turn_number
        )

        # Use full conversation history for context-aware responses
        messages = session.get_openai_messages()
        messages.append({"role": "user", "content": counter_prompt})

        return await self.openai.chat_completion(messages)

    async def get_session_summary(self, session_id: str) -> SessionSummaryResponse:
        """Generate a summary of the debate session."""
        session = self.memory.get_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found or has expired")

        summary_prompt = self.prompts.get_summary_prompt(
            session.topic, session.side, session.conversation_history
        )
        messages = [
            {
                "role": "system",
                "content": "You are an objective debate analyst. Provide concise, balanced summaries.",
            },
            {"role": "user", "content": summary_prompt},
        ]

        summary = await self.openai.chat_completion(messages, temperature=0.4)

        return SessionSummaryResponse(
            session_id=session_id,
            topic=session.topic,
            side=session.side,
            total_turns=session.turn_number,
            conversation_history=session.message_log,
            summary=summary,
        )

    def end_session(self, session_id: str) -> bool:
        """End and clean up a debate session."""
        return self.memory.delete_session(session_id)

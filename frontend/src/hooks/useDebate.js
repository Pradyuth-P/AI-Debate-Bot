import { useState, useCallback, useRef } from "react";
import { debateApi } from "../services/debateApi";

export const DEBATE_STATUS = {
  IDLE: "idle",
  STARTING: "starting",
  ACTIVE: "active",
  SENDING: "sending",
  ENDING: "ending",
  ENDED: "ended",
  ERROR: "error",
};

export const MESSAGE_TYPE = {
  SYSTEM: "system",
  AI_OPENING: "ai_opening",
  USER: "user",
  AI_COUNTER: "ai_counter",
  SUMMARY: "summary",
};

const createMessage = (type, content, metadata = {}) => ({
  id: `msg_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
  type,
  content,
  timestamp: new Date(),
  ...metadata,
});

export function useDebate() {
  const [status, setStatus] = useState(DEBATE_STATUS.IDLE);
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [topic, setTopic] = useState("");
  const [side, setSide] = useState(null);
  const [error, setError] = useState(null);
  const [turnNumber, setTurnNumber] = useState(0);
  const abortRef = useRef(null);

  const clearError = useCallback(() => setError(null), []);

  const addMessage = useCallback((type, content, metadata = {}) => {
    const msg = createMessage(type, content, metadata);
    setMessages((prev) => [...prev, msg]);
    return msg;
  }, []);

  const startDebate = useCallback(
    async (debateTopic, debateSide) => {
      setStatus(DEBATE_STATUS.STARTING);
      setError(null);
      setMessages([]);

      try {
        const response = await debateApi.startDebate(debateTopic, debateSide);

        setSessionId(response.session_id);
        setTopic(response.topic);
        setSide(response.side);
        setTurnNumber(1);

        // Add system message
        addMessage(
          MESSAGE_TYPE.SYSTEM,
          `Debate started: "${response.topic}" — AI is arguing ${response.side}`,
          { topic: response.topic, side: response.side }
        );

        // Add AI opening argument
        addMessage(MESSAGE_TYPE.AI_OPENING, response.opening_argument, {
          side: response.side,
          turnNumber: 1,
        });

        setStatus(DEBATE_STATUS.ACTIVE);
      } catch (err) {
        setError(err.message || "Failed to start debate. Please try again.");
        setStatus(DEBATE_STATUS.ERROR);
      }
    },
    [addMessage]
  );

  const sendArgument = useCallback(
    async (userArgument) => {
      if (!sessionId || status !== DEBATE_STATUS.ACTIVE) return;

      setStatus(DEBATE_STATUS.SENDING);
      setError(null);

      // Add user message immediately
      addMessage(MESSAGE_TYPE.USER, userArgument);

      try {
        const response = await debateApi.sendArgument(sessionId, userArgument);

        setTurnNumber(response.turn_number);

        // Add AI counter-argument with analysis
        addMessage(MESSAGE_TYPE.AI_COUNTER, response.counter_argument, {
          analysis: response.analysis,
          turnNumber: response.turn_number,
          side: response.side,
        });

        setStatus(DEBATE_STATUS.ACTIVE);
      } catch (err) {
        setError(err.message || "Failed to get AI response. Please try again.");
        setStatus(DEBATE_STATUS.ACTIVE); // Allow retry
      }
    },
    [sessionId, status, addMessage]
  );

  const endDebate = useCallback(async () => {
    if (!sessionId) return;

    setStatus(DEBATE_STATUS.ENDING);

    try {
      const summary = await debateApi.getSessionSummary(sessionId);
      addMessage(MESSAGE_TYPE.SUMMARY, summary.summary, {
        totalTurns: summary.total_turns,
        topic: summary.topic,
        side: summary.side,
      });

      await debateApi.endSession(sessionId).catch(() => {}); // Best effort
    } catch {
      // Still end even if summary fails
    }

    setStatus(DEBATE_STATUS.ENDED);
  }, [sessionId, addMessage]);

  const resetDebate = useCallback(() => {
    setStatus(DEBATE_STATUS.IDLE);
    setMessages([]);
    setSessionId(null);
    setTopic("");
    setSide(null);
    setError(null);
    setTurnNumber(0);
  }, []);

  return {
    // State
    status,
    messages,
    sessionId,
    topic,
    side,
    error,
    turnNumber,
    // Computed
    isLoading:
      status === DEBATE_STATUS.STARTING || status === DEBATE_STATUS.SENDING,
    isActive: status === DEBATE_STATUS.ACTIVE,
    isEnded: status === DEBATE_STATUS.ENDED,
    isIdle: status === DEBATE_STATUS.IDLE,
    // Actions
    startDebate,
    sendArgument,
    endDebate,
    resetDebate,
    clearError,
  };
}

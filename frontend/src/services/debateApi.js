import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60s for AI responses
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
);

// Response interceptor with error normalization
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "An unexpected error occurred";

    const normalizedError = new Error(message);
    normalizedError.status = error.response?.status;
    normalizedError.originalError = error;
    return Promise.reject(normalizedError);
  }
);

export const debateApi = {
  /**
   * Start a new debate session
   * @param {string} topic - Debate topic
   * @param {"FOR"|"AGAINST"} side - AI's side
   * @returns {Promise<StartDebateResponse>}
   */
  startDebate: (topic, side) =>
    api.post("/debate/start", { topic, side }),

  /**
   * Send a user argument and get AI counter-argument
   * @param {string} sessionId - Session ID
   * @param {string} userArgument - User's argument text
   * @returns {Promise<DebateMessageResponse>}
   */
  sendArgument: (sessionId, userArgument) =>
    api.post("/debate/message", {
      session_id: sessionId,
      user_argument: userArgument,
    }),

  /**
   * Get session summary
   * @param {string} sessionId - Session ID
   * @returns {Promise<SessionSummaryResponse>}
   */
  getSessionSummary: (sessionId) =>
    api.get(`/debate/session/${sessionId}`),

  /**
   * End a debate session
   * @param {string} sessionId - Session ID
   */
  endSession: (sessionId) =>
    api.delete(`/debate/session/${sessionId}`),

  /**
   * Health check
   */
  healthCheck: () => api.get("/health"),
};

export default api;

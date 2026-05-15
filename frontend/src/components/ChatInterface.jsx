import { DEBATE_STATUS } from "../hooks/useDebate";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import ChatInput from "./ChatInput";
import ChatHeader from "./ChatHeader";
import ErrorBanner from "./ErrorBanner";
import { useAutoScroll } from "../hooks/useAutoScroll";

export default function ChatInterface({
  messages,
  status,
  topic,
  side,
  turnNumber,
  error,
  onSendArgument,
  onEndDebate,
  onReset,
  onClearError,
}) {
  const isLoading = status === DEBATE_STATUS.SENDING || status === DEBATE_STATUS.STARTING;
  const isEnded = status === DEBATE_STATUS.ENDED;
  const isEnding = status === DEBATE_STATUS.ENDING;

  const { containerRef } = useAutoScroll(messages.length);

  return (
    <div className="flex flex-col h-screen bg-debate-bg">
      {/* Fixed header */}
      <ChatHeader
        topic={topic}
        side={side}
        turnNumber={turnNumber}
        onEnd={onEndDebate}
        onReset={onReset}
        isEnded={isEnded || isEnding}
      />

      {/* Error banner */}
      {error && (
        <div className="px-4 py-2 max-w-4xl w-full mx-auto">
          <ErrorBanner error={error} onDismiss={onClearError} />
        </div>
      )}

      {/* Scrollable message area */}
      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto px-4 py-6"
      >
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}

          {/* Typing indicator */}
          {(isLoading || isEnding) && (
            <TypingIndicator side={side} />
          )}

          {/* Ended state */}
          {isEnded && (
            <div className="flex justify-center my-6">
              <div className="flex items-center gap-3 px-5 py-2.5 rounded-full bg-debate-card border border-debate-border">
                <span className="w-2 h-2 rounded-full bg-debate-muted" />
                <span className="text-sm text-debate-muted font-body">Debate concluded</span>
                <button
                  onClick={onReset}
                  className="ml-2 text-debate-accent text-sm font-semibold hover:text-indigo-400 transition-colors"
                >
                  Start new →
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Fixed input area */}
      {!isEnded && (
        <ChatInput
          onSend={onSendArgument}
          isDisabled={isLoading || isEnding || status !== DEBATE_STATUS.ACTIVE}
          side={side}
        />
      )}

      {/* Ended: show reset prompt */}
      {isEnded && (
        <div className="border-t border-debate-border bg-debate-surface/80 backdrop-blur-sm px-4 py-4">
          <div className="max-w-4xl mx-auto flex justify-center">
            <button
              onClick={onReset}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-debate-accent to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-white font-display font-semibold text-sm transition-all duration-300 hover:-translate-y-0.5 shadow-lg shadow-debate-accent/20"
            >
              ↻ Start a New Debate
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

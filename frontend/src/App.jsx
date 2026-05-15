import { useDebate, DEBATE_STATUS } from "./hooks/useDebate";
import TopicSetup from "./components/TopicSetup";
import ChatInterface from "./components/ChatInterface";

export default function App() {
  const {
    status,
    messages,
    topic,
    side,
    error,
    turnNumber,
    isLoading,
    isIdle,
    startDebate,
    sendArgument,
    endDebate,
    resetDebate,
    clearError,
  } = useDebate();

  return (
    <>
      {/* Noise texture overlay */}
      <div className="noise-overlay" />

      {isIdle || status === DEBATE_STATUS.ERROR ? (
        <TopicSetup onStart={startDebate} isLoading={isLoading} />
      ) : (
        <ChatInterface
          messages={messages}
          status={status}
          topic={topic}
          side={side}
          turnNumber={turnNumber}
          error={error}
          onSendArgument={sendArgument}
          onEndDebate={endDebate}
          onReset={resetDebate}
          onClearError={clearError}
        />
      )}
    </>
  );
}

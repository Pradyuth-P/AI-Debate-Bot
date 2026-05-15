export default function TypingIndicator({ side }) {
  const sideColorHex = side === "FOR" ? "#22C55E" : "#EF4444";

  return (
    <div className="flex gap-3 mb-4 animate-fade-in">
      {/* AI Avatar */}
      <div className="flex-shrink-0 mt-1">
        <div
          className="w-8 h-8 rounded-full flex items-center justify-center border animate-pulse-slow"
          style={{
            backgroundColor: `${sideColorHex}15`,
            borderColor: `${sideColorHex}40`,
          }}
        >
          <svg
            className="w-4 h-4"
            style={{ color: sideColorHex }}
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path d="M16.56 11.166A8.373 8.373 0 0 0 17 8.5c0-4.694-3.806-8.5-8.5-8.5C3.806 0 0 3.806 0 8.5c0 4.271 3.125 7.817 7.227 8.439l.313.046V20l2.457-1.637.11-.073C13.522 17.025 16.56 14.348 16.56 11.166Z" />
          </svg>
        </div>
      </div>

      {/* Typing bubble */}
      <div className="bg-debate-card border border-debate-border rounded-2xl rounded-tl-sm px-5 py-4">
        <div className="flex items-center gap-1.5">
          <div className="typing-dot" />
          <div className="typing-dot" />
          <div className="typing-dot" />
        </div>
        <p className="text-xs text-debate-muted mt-2">AI is formulating a response…</p>
      </div>
    </div>
  );
}

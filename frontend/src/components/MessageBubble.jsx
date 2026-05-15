import { MESSAGE_TYPE } from "../hooks/useDebate";

function ArgumentRating({ analysis }) {
  if (!analysis) return null;
  const { rating, strength, key_points, logical_fallacies } = analysis;
  const ratingColor =
    rating >= 7 ? "#22C55E" : rating >= 4 ? "#F59E0B" : "#EF4444";
  const ratingLabel =
    rating >= 7 ? "Strong" : rating >= 4 ? "Moderate" : "Weak";

  return (
    <div className="mt-4 pt-4 border-t border-debate-border/50 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-debate-muted uppercase tracking-wider">
          Argument Analysis
        </span>
        <span
          className="text-xs font-mono font-bold px-2 py-0.5 rounded-md"
          style={{ color: ratingColor, backgroundColor: `${ratingColor}20` }}
        >
          {ratingLabel} · {rating}/10
        </span>
      </div>

      {/* Rating bar */}
      <div className="h-1.5 bg-debate-border rounded-full overflow-hidden">
        <div
          className="h-full rounded-full rating-fill"
          style={{
            width: `${rating * 10}%`,
            backgroundColor: ratingColor,
          }}
        />
      </div>

      {/* Strength */}
      <p className="text-xs text-debate-muted italic">"{strength}"</p>

      {/* Key points */}
      {key_points?.length > 0 && (
        <div className="space-y-1">
          {key_points.map((point, i) => (
            <div key={i} className="flex items-start gap-2">
              <span className="text-debate-accent text-xs mt-0.5">▸</span>
              <span className="text-xs text-debate-muted">{point}</span>
            </div>
          ))}
        </div>
      )}

      {/* Logical fallacies */}
      {logical_fallacies?.length > 0 && (
        <div className="flex items-start gap-2">
          <span className="text-debate-against text-xs">⚠</span>
          <span className="text-xs text-debate-against/80">
            {logical_fallacies.join(", ")}
          </span>
        </div>
      )}
    </div>
  );
}

function formatTimestamp(date) {
  return new Intl.DateTimeFormat("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  }).format(date instanceof Date ? date : new Date(date));
}

export default function MessageBubble({ message }) {
  const { type, content, timestamp, analysis, side, turnNumber, totalTurns } =
    message;

  // System message
  if (type === MESSAGE_TYPE.SYSTEM) {
    return (
      <div className="flex justify-center my-4 message-enter">
        <div className="flex items-center gap-3 px-4 py-2 rounded-full bg-debate-card border border-debate-border">
          <span className="w-2 h-2 rounded-full bg-debate-accent animate-pulse" />
          <span className="text-xs text-debate-muted font-body">{content}</span>
        </div>
      </div>
    );
  }

  // Summary message
  if (type === MESSAGE_TYPE.SUMMARY) {
    return (
      <div className="my-6 message-enter">
        <div className="glass-card rounded-2xl p-6 border border-debate-gold/30">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-lg bg-debate-gold/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-debate-gold" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401Z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h3 className="font-display font-bold text-debate-text">Debate Summary</h3>
              <p className="text-xs text-debate-muted">{totalTurns} exchanges completed</p>
            </div>
          </div>
          <p className="text-debate-text/80 font-body text-sm leading-relaxed">{content}</p>
        </div>
      </div>
    );
  }

  // User message
  if (type === MESSAGE_TYPE.USER) {
    return (
      <div className="flex justify-end gap-3 mb-6 message-enter">
        <div className="max-w-[80%]">
          <div className="bg-debate-accent/20 border border-debate-accent/30 rounded-2xl rounded-br-sm px-5 py-4">
            <p className="text-debate-text font-body text-sm leading-relaxed whitespace-pre-wrap">
              {content}
            </p>
          </div>
          <p className="text-right text-xs text-debate-muted/50 mt-1.5 font-body">
            You · {formatTimestamp(timestamp)}
          </p>
        </div>
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-debate-accent/20 border border-debate-accent/40 flex items-center justify-center mt-1">
          <svg className="w-4 h-4 text-debate-accent" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM3.465 14.493a1.23 1.23 0 0 0 .41 1.412A9.957 9.957 0 0 0 10 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 0 0-13.074.003Z" />
          </svg>
        </div>
      </div>
    );
  }

  // AI messages (opening + counter)
  const isOpening = type === MESSAGE_TYPE.AI_OPENING;
  const sideColor = side === "FOR" ? "debate-for" : "debate-against";
  const sideColorHex = side === "FOR" ? "#22C55E" : "#EF4444";
  const sideLabel = side === "FOR" ? "FOR" : "AGAINST";
  const headerLabel = isOpening
    ? `Opening Argument — ${sideLabel}`
    : `Counter-Argument #${turnNumber - 1} — ${sideLabel}`;

  return (
    <div className="flex gap-3 mb-6 message-enter">
      {/* AI Avatar */}
      <div className="flex-shrink-0 mt-1">
        <div
          className="w-8 h-8 rounded-full flex items-center justify-center border"
          style={{
            backgroundColor: `${sideColorHex}15`,
            borderColor: `${sideColorHex}40`,
          }}
        >
          <svg className="w-4 h-4" style={{ color: sideColorHex }} viewBox="0 0 20 20" fill="currentColor">
            <path d="M16.56 11.166A8.373 8.373 0 0 0 17 8.5c0-4.694-3.806-8.5-8.5-8.5C3.806 0 0 3.806 0 8.5c0 4.271 3.125 7.817 7.227 8.439l.313.046V20l2.457-1.637.11-.073C13.522 17.025 16.56 14.348 16.56 11.166Z" />
          </svg>
        </div>
      </div>

      {/* Message content */}
      <div className="flex-1 max-w-[85%]">
        {/* Header */}
        <div className="flex items-center gap-2 mb-2">
          <span
            className="text-xs font-semibold font-mono px-2 py-0.5 rounded-md"
            style={{
              color: sideColorHex,
              backgroundColor: `${sideColorHex}15`,
            }}
          >
            {headerLabel}
          </span>
          {isOpening && (
            <span className="text-xs text-debate-muted/50">Opening</span>
          )}
        </div>

        {/* Bubble */}
        <div className="bg-debate-card border border-debate-border rounded-2xl rounded-tl-sm px-5 py-4">
          <div className="prose-debate text-debate-text/90 font-body text-sm leading-relaxed whitespace-pre-wrap">
            {content}
          </div>

          {/* Analysis panel */}
          {analysis && <ArgumentRating analysis={analysis} />}
        </div>

        <p className="text-xs text-debate-muted/50 mt-1.5 font-body">
          AI Debater · {formatTimestamp(timestamp)}
        </p>
      </div>
    </div>
  );
}

import { useState, useRef, useEffect } from "react";

export default function ChatInput({ onSend, isDisabled, side }) {
  const [input, setInput] = useState("");
  const textareaRef = useRef(null);
  const maxLength = 2000;

  useEffect(() => {
    if (!isDisabled && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [isDisabled]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [input]);

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed || isDisabled) return;
    onSend(trimmed);
    setInput("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const charPercent = (input.length / maxLength) * 100;
  const isNearLimit = input.length > maxLength * 0.8;
  const isAtLimit = input.length >= maxLength;
  const sideLabel = side === "FOR" ? "against" : "in favor of";

  return (
    <div className="border-t border-debate-border bg-debate-surface/80 backdrop-blur-sm px-4 py-4">
      <div className="max-w-4xl mx-auto">
        {/* Hint */}
        <p className="text-xs text-debate-muted/50 mb-2 text-center font-body">
          Argue {sideLabel} the topic · Press{" "}
          <kbd className="px-1.5 py-0.5 rounded bg-debate-border text-debate-muted font-mono text-[10px]">
            Enter
          </kbd>{" "}
          to send ·{" "}
          <kbd className="px-1.5 py-0.5 rounded bg-debate-border text-debate-muted font-mono text-[10px]">
            Shift+Enter
          </kbd>{" "}
          for newline
        </p>

        {/* Input area */}
        <div
          className={`
            flex items-end gap-3 bg-debate-card rounded-2xl border transition-all duration-200 p-3
            ${isDisabled
              ? "border-debate-border opacity-60"
              : "border-debate-border-bright focus-within:border-debate-accent/50 focus-within:ring-2 focus-within:ring-debate-accent/10"
            }
          `}
        >
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value.slice(0, maxLength))}
            onKeyDown={handleKeyDown}
            placeholder={isDisabled ? "AI is responding…" : "Make your argument…"}
            disabled={isDisabled}
            rows={1}
            className="flex-1 bg-transparent text-debate-text placeholder-debate-muted/40 font-body text-sm resize-none focus:outline-none leading-relaxed min-h-[24px]"
          />

          {/* Send button */}
          <button
            onClick={handleSend}
            disabled={isDisabled || !input.trim()}
            className={`
              flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-200
              ${!isDisabled && input.trim()
                ? "bg-debate-accent hover:bg-indigo-400 text-white shadow-md shadow-debate-accent/20 hover:-translate-y-0.5 active:translate-y-0"
                : "bg-debate-border text-debate-muted cursor-not-allowed"
              }
            `}
          >
            {isDisabled ? (
              <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
            ) : (
              <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
                <path d="M3.105 2.288a.75.75 0 0 0-.826.95l1.414 4.926A1.5 1.5 0 0 0 5.135 9.25h6.115a.75.75 0 0 1 0 1.5H5.135a1.5 1.5 0 0 0-1.442 1.086l-1.414 4.926a.75.75 0 0 0 .826.95 28.897 28.897 0 0 0 15.293-7.155.75.75 0 0 0 0-1.114A28.897 28.897 0 0 0 3.105 2.288Z" />
              </svg>
            )}
          </button>
        </div>

        {/* Character counter */}
        {isNearLimit && (
          <div className="flex items-center justify-between mt-2">
            <div className="flex-1 h-0.5 bg-debate-border rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-200"
                style={{
                  width: `${charPercent}%`,
                  backgroundColor: isAtLimit ? "#EF4444" : isNearLimit ? "#F59E0B" : "#22C55E",
                }}
              />
            </div>
            <span
              className={`ml-3 text-xs font-mono ${isAtLimit ? "text-debate-against" : "text-debate-gold"}`}
            >
              {input.length}/{maxLength}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

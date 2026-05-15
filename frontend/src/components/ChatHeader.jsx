export default function ChatHeader({ topic, side, turnNumber, onEnd, onReset, isEnded }) {
  const sideColor = side === "FOR" ? "#22C55E" : "#EF4444";
  const sideBg = side === "FOR" ? "#22C55E15" : "#EF444415";
  const sideBorder = side === "FOR" ? "#22C55E40" : "#EF444440";

  return (
    <div className="border-b border-debate-border bg-debate-surface/90 backdrop-blur-sm px-4 py-3 flex-shrink-0">
      <div className="max-w-4xl mx-auto flex items-center justify-between gap-4">
        {/* Left: debate info */}
        <div className="flex items-center gap-3 min-w-0">
          <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-debate-card border border-debate-border flex items-center justify-center">
            <svg className="w-4 h-4 text-debate-accent" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 2a6 6 0 0 0-6 6v.75a.75.75 0 0 0 .5.707l.97.323A1.5 1.5 0 0 0 7.5 9.25h5a1.5 1.5 0 0 0 2.03-.47l.97-.323A.75.75 0 0 0 16 7.75V8a6 6 0 0 0-6-6ZM4.25 10.5a.75.75 0 0 0-.75.75v.25c0 2.392 1.662 4.396 3.908 4.895a.75.75 0 0 0 .592-1.374A3.502 3.502 0 0 1 5 11.5v-.25a.75.75 0 0 0-.75-.75Zm11.5 0a.75.75 0 0 0-.75.75v.25a3.502 3.502 0 0 1-3 3.47.75.75 0 0 0 .592 1.375C14.838 15.896 16.5 13.892 16.5 11.5v-.25a.75.75 0 0 0-.75-.75Z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="min-w-0">
            <p className="text-xs text-debate-muted font-body truncate">Active Debate</p>
            <h2 className="text-sm font-semibold text-debate-text font-body truncate">
              {topic}
            </h2>
          </div>
        </div>

        {/* Center: side badge + turn counter */}
        <div className="flex items-center gap-3 flex-shrink-0">
          <div
            className="px-3 py-1 rounded-full text-xs font-semibold font-mono border"
            style={{
              color: sideColor,
              backgroundColor: sideBg,
              borderColor: sideBorder,
            }}
          >
            AI: {side}
          </div>
          <div className="text-xs text-debate-muted font-mono bg-debate-card border border-debate-border px-2 py-1 rounded-lg">
            Turn {turnNumber}
          </div>
        </div>

        {/* Right: actions */}
        <div className="flex items-center gap-2 flex-shrink-0">
          {!isEnded ? (
            <button
              onClick={onEnd}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-debate-card border border-debate-border hover:border-debate-gold/50 hover:text-debate-gold text-debate-muted text-xs font-body transition-all duration-200"
            >
              <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16ZM8 7a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1V8a1 1 0 0 0-1-1H8Z" clipRule="evenodd" />
              </svg>
              End
            </button>
          ) : null}
          <button
            onClick={onReset}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-debate-card border border-debate-border hover:border-debate-accent/50 hover:text-debate-accent text-debate-muted text-xs font-body transition-all duration-200"
          >
            <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M15.312 11.424a5.5 5.5 0 0 1-9.201 2.466l-.312-.311h2.433a.75.75 0 0 0 0-1.5H3.989a.75.75 0 0 0-.75.75v4.242a.75.75 0 0 0 1.5 0v-2.43l.31.31a7 7 0 0 0 11.712-3.138.75.75 0 0 0-1.449-.39Zm1.23-3.723a.75.75 0 0 0 .219-.53V2.929a.75.75 0 0 0-1.5 0V5.36l-.31-.31A7 7 0 0 0 3.239 8.188a.75.75 0 1 0 1.448.389A5.5 5.5 0 0 1 13.89 6.11l.311.31h-2.432a.75.75 0 0 0 0 1.5h4.243a.75.75 0 0 0 .53-.219Z" clipRule="evenodd" />
            </svg>
            New
          </button>
        </div>
      </div>
    </div>
  );
}

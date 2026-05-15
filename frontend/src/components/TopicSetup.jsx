import { useState } from "react";

const EXAMPLE_TOPICS = [
  "AI will replace most human jobs within 20 years",
  "Social media does more harm than good to society",
  "Universal Basic Income should be implemented globally",
  "Space colonization should be humanity's top priority",
  "Nuclear energy is essential for a sustainable future",
  "Remote work should become the permanent default",
];

export default function TopicSetup({ onStart, isLoading }) {
  const [topic, setTopic] = useState("");
  const [side, setSide] = useState(null);
  const [topicError, setTopicError] = useState("");

  const handleStart = () => {
    if (!topic.trim()) {
      setTopicError("Please enter a debate topic");
      return;
    }
    if (topic.trim().length < 5) {
      setTopicError("Topic must be at least 5 characters");
      return;
    }
    if (!side) {
      setTopicError("Please select which side the AI should argue");
      return;
    }
    setTopicError("");
    onStart(topic.trim(), side);
  };

  const handleTopicChange = (e) => {
    setTopic(e.target.value);
    if (topicError) setTopicError("");
  };

  const handleExampleClick = (exampleTopic) => {
    setTopic(exampleTopic);
    if (topicError) setTopicError("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleStart();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 py-12">
      {/* Background glow effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-debate-accent/5 blur-3xl" />
        <div className="absolute bottom-1/4 left-1/4 w-80 h-80 rounded-full bg-debate-for/5 blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full bg-debate-against/5 blur-3xl" />
      </div>

      <div className="relative w-full max-w-2xl animate-fade-in">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-debate-card border border-debate-border mb-6 relative">
            <svg className="w-8 h-8 text-debate-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
            </svg>
            <div className="absolute inset-0 rounded-2xl shimmer" />
          </div>
          <h1 className="font-display text-5xl font-bold text-debate-text mb-3">
            AI Debate Bot
          </h1>
          <p className="text-debate-muted text-lg font-body">
            Sharpen your arguments against a world-class AI debater
          </p>
        </div>

        {/* Main card */}
        <div className="glass-card rounded-3xl p-8 space-y-8">
          {/* Topic input */}
          <div>
            <label className="block text-sm font-semibold text-debate-text/70 uppercase tracking-wider mb-3">
              Debate Topic
            </label>
            <textarea
              value={topic}
              onChange={handleTopicChange}
              onKeyDown={handleKeyDown}
              placeholder="Enter a controversial topic to debate..."
              rows={3}
              className="w-full bg-debate-bg border border-debate-border focus:border-debate-accent rounded-2xl px-5 py-4 text-debate-text placeholder-debate-muted/50 font-body text-base resize-none focus:outline-none focus:ring-2 focus:ring-debate-accent/20 transition-all duration-200"
              disabled={isLoading}
            />
            {topicError && (
              <p className="mt-2 text-debate-against text-sm font-medium animate-fade-in">
                ⚠ {topicError}
              </p>
            )}
          </div>

          {/* Example topics */}
          <div>
            <label className="block text-xs font-semibold text-debate-muted uppercase tracking-wider mb-3">
              Example Topics
            </label>
            <div className="flex flex-wrap gap-2">
              {EXAMPLE_TOPICS.map((exTopic) => (
                <button
                  key={exTopic}
                  onClick={() => handleExampleClick(exTopic)}
                  disabled={isLoading}
                  className="px-3 py-1.5 rounded-lg bg-debate-bg border border-debate-border hover:border-debate-accent/50 text-debate-muted hover:text-debate-text text-xs font-body transition-all duration-200 disabled:opacity-50"
                >
                  {exTopic.length > 40 ? exTopic.slice(0, 40) + "…" : exTopic}
                </button>
              ))}
            </div>
          </div>

          {/* Side selection */}
          <div>
            <label className="block text-sm font-semibold text-debate-text/70 uppercase tracking-wider mb-4">
              AI Argues...
            </label>
            <div className="grid grid-cols-2 gap-4">
              {/* FOR button */}
              <button
                onClick={() => setSide("FOR")}
                disabled={isLoading}
                className={`
                  relative group p-5 rounded-2xl border-2 transition-all duration-300 text-left
                  ${side === "FOR"
                    ? "border-debate-for bg-debate-for/10 animate-glow-for"
                    : "border-debate-border bg-debate-bg hover:border-debate-for/40 hover:bg-debate-for/5"
                  }
                  disabled:opacity-50 disabled:cursor-not-allowed
                `}
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className={`w-3 h-3 rounded-full transition-all duration-300 ${side === "FOR" ? "bg-debate-for shadow-lg shadow-debate-for/50" : "bg-debate-border"}`} />
                  <span className="font-display text-xl font-bold text-debate-for">FOR</span>
                </div>
                <p className="text-xs text-debate-muted font-body">
                  AI argues in favor of the topic. You argue against it.
                </p>
                {side === "FOR" && (
                  <div className="absolute top-3 right-3">
                    <svg className="w-4 h-4 text-debate-for" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" />
                    </svg>
                  </div>
                )}
              </button>

              {/* AGAINST button */}
              <button
                onClick={() => setSide("AGAINST")}
                disabled={isLoading}
                className={`
                  relative group p-5 rounded-2xl border-2 transition-all duration-300 text-left
                  ${side === "AGAINST"
                    ? "border-debate-against bg-debate-against/10 animate-glow-against"
                    : "border-debate-border bg-debate-bg hover:border-debate-against/40 hover:bg-debate-against/5"
                  }
                  disabled:opacity-50 disabled:cursor-not-allowed
                `}
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className={`w-3 h-3 rounded-full transition-all duration-300 ${side === "AGAINST" ? "bg-debate-against shadow-lg shadow-debate-against/50" : "bg-debate-border"}`} />
                  <span className="font-display text-xl font-bold text-debate-against">AGAINST</span>
                </div>
                <p className="text-xs text-debate-muted font-body">
                  AI argues against the topic. You argue in favor of it.
                </p>
                {side === "AGAINST" && (
                  <div className="absolute top-3 right-3">
                    <svg className="w-4 h-4 text-debate-against" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" />
                    </svg>
                  </div>
                )}
              </button>
            </div>
          </div>

          {/* Start button */}
          <button
            onClick={handleStart}
            disabled={isLoading || !topic.trim() || !side}
            className={`
              w-full py-4 rounded-2xl font-display font-semibold text-lg transition-all duration-300
              ${isLoading
                ? "bg-debate-border text-debate-muted cursor-not-allowed"
                : topic.trim() && side
                  ? "bg-gradient-to-r from-debate-accent to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-white shadow-lg shadow-debate-accent/20 hover:shadow-debate-accent/30 hover:-translate-y-0.5 active:translate-y-0"
                  : "bg-debate-border/50 text-debate-muted/50 cursor-not-allowed"
              }
            `}
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-3">
                <svg className="animate-spin w-5 h-5" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Preparing the debate arena…
              </span>
            ) : (
              "Start Debate →"
            )}
          </button>
        </div>

        {/* Footer note */}
        <p className="text-center text-debate-muted/50 text-xs mt-6 font-body">
          Powered by OpenAI GPT-4 · Your arguments vs world-class AI rhetoric
        </p>
      </div>
    </div>
  );
}

export default function ErrorBanner({ error, onDismiss }) {
  if (!error) return null;

  return (
    <div className="mx-4 my-2 max-w-4xl mx-auto animate-slide-up">
      <div className="flex items-start gap-3 bg-debate-against/10 border border-debate-against/30 rounded-xl px-4 py-3">
        <svg
          className="w-4 h-4 text-debate-against flex-shrink-0 mt-0.5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Zm-8-5a.75.75 0 0 1 .75.75v4.5a.75.75 0 0 1-1.5 0v-4.5A.75.75 0 0 1 10 5Zm0 10a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z"
            clipRule="evenodd"
          />
        </svg>
        <div className="flex-1 min-w-0">
          <p className="text-sm text-debate-against font-semibold">Error</p>
          <p className="text-xs text-debate-against/70 mt-0.5">{error}</p>
        </div>
        <button
          onClick={onDismiss}
          className="text-debate-against/50 hover:text-debate-against transition-colors"
        >
          <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
            <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
          </svg>
        </button>
      </div>
    </div>
  );
}

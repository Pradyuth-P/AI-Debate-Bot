/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Playfair Display'", "Georgia", "serif"],
        body: ["'DM Sans'", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        debate: {
          bg: "#0A0A0F",
          surface: "#111118",
          card: "#1A1A24",
          border: "#2A2A3A",
          "border-bright": "#3A3A50",
          for: "#22C55E",
          "for-dim": "#166534",
          against: "#EF4444",
          "against-dim": "#7F1D1D",
          gold: "#F59E0B",
          "gold-dim": "#78350F",
          text: "#E2E8F0",
          muted: "#64748B",
          accent: "#818CF8",
        },
      },
      animation: {
        "fade-in": "fadeIn 0.4s ease-out",
        "slide-up": "slideUp 0.4s ease-out",
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        typing: "typing 1.2s steps(3) infinite",
        "glow-for": "glowFor 2s ease-in-out infinite alternate",
        "glow-against": "glowAgainst 2s ease-in-out infinite alternate",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        typing: {
          "0%": { content: "'●'" },
          "33%": { content: "'● ●'" },
          "66%": { content: "'● ● ●'" },
          "100%": { content: "'●'" },
        },
        glowFor: {
          "0%": { boxShadow: "0 0 5px #22C55E40" },
          "100%": { boxShadow: "0 0 20px #22C55E80, 0 0 40px #22C55E30" },
        },
        glowAgainst: {
          "0%": { boxShadow: "0 0 5px #EF444440" },
          "100%": { boxShadow: "0 0 20px #EF444480, 0 0 40px #EF444430" },
        },
      },
    },
  },
  plugins: [],
};

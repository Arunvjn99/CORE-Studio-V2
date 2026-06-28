import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      // ── Core Studio Design Tokens ─────────────────────────────────────────
      colors: {
        // Brand
        brand: {
          50: "#f0f4ff",
          100: "#dde6ff",
          200: "#c0ccff",
          300: "#9aaaff",
          400: "#7b87ff",
          500: "#5b5ef4",
          600: "#4a4de0",
          700: "#3b3db5",
          800: "#303490",
          900: "#2a2d73",
        },
        // Accent — warm coral
        accent: {
          DEFAULT: "#FF4D4F",
          50: "#fff1f1",
          100: "#ffe0e0",
          500: "#FF4D4F",
          600: "#e63b3d",
        },
        // Neutral surface system
        surface: {
          0: "#ffffff",
          50: "#fafafa",
          100: "#f5f5f5",
          200: "#ebebeb",
          300: "#d6d6d6",
          400: "#a3a3a3",
          500: "#737373",
          600: "#525252",
          700: "#404040",
          800: "#262626",
          900: "#171717",
          950: "#0a0a0a",
        },
        // Agent identity colors
        agent: {
          planner: "#8B5CF6",
          ux:      "#0EA5E9",
          ui:      "#10B981",
          review:  "#F59E0B",
        },
        // Status
        status: {
          pending:  "#94A3B8",
          running:  "#3B82F6",
          approved: "#10B981",
          rejected: "#EF4444",
          waiting:  "#F59E0B",
        },
        // shadcn/Radix semantic (HSL vars — keep for component compat)
        border:     "hsl(var(--border))",
        input:      "hsl(var(--input))",
        ring:       "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT:    "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT:    "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT:    "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        card: {
          DEFAULT:    "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },

        // ── Semantic token utilities (map to --cs-* CSS vars) ─────────────
        // Usage: bg-cs-surface, text-cs-muted, border-cs-border, etc.
        cs: {
          // Brand
          primary:        "var(--cs-primary)",
          "primary-hover": "var(--cs-primary-hover)",
          "primary-light": "var(--cs-primary-light)",
          "primary-subtle":"var(--cs-primary-subtle)",
          // Surfaces
          bg:             "var(--cs-bg)",
          "surface":      "var(--cs-surface)",
          "surface-subtle":"var(--cs-surface-subtle)",
          "surface-muted": "var(--cs-surface-muted)",
          "surface-overlay":"var(--cs-surface-overlay)",
          // Text
          text:           "var(--cs-text)",
          "text-secondary":"var(--cs-text-secondary)",
          "text-tertiary": "var(--cs-text-tertiary)",
          "text-soft":    "var(--cs-text-soft)",
          "text-faint":   "var(--cs-text-faint)",
          // Borders
          border:         "var(--cs-border)",
          "border-strong":"var(--cs-border-strong)",
          "border-soft":  "var(--cs-border-soft)",
          // Status
          success:        "var(--cs-success)",
          "success-surface":"var(--cs-success-surface)",
          warning:        "var(--cs-warning)",
          "warning-surface":"var(--cs-warning-surface)",
          danger:         "var(--cs-danger)",
          "danger-surface":"var(--cs-danger-surface)",
          info:           "var(--cs-info)",
          "info-surface": "var(--cs-info-surface)",
        },
      },

      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },

      fontSize: {
        "2xs": ["10px", { lineHeight: "14px" }],
        xs:    ["12px", { lineHeight: "16px" }],
        sm:    ["13px", { lineHeight: "20px" }],
        base:  ["14px", { lineHeight: "22px" }],
        md:    ["15px", { lineHeight: "24px" }],
        lg:    ["16px", { lineHeight: "26px" }],
        xl:    ["18px", { lineHeight: "28px" }],
        "2xl": ["20px", { lineHeight: "30px" }],
        "3xl": ["24px", { lineHeight: "32px" }],
        "4xl": ["30px", { lineHeight: "38px" }],
        "5xl": ["36px", { lineHeight: "44px" }],
        // Exact UI sizes from design token spec
        "ui-9":    ["9px",    { lineHeight: "14px" }],
        "ui-10":   ["10px",   { lineHeight: "14px" }],
        "ui-10_5": ["10.5px", { lineHeight: "14px" }],
        "ui-11":   ["11px",   { lineHeight: "16px" }],
        "ui-11_5": ["11.5px", { lineHeight: "16px" }],
        "ui-12_5": ["12.5px", { lineHeight: "18px" }],
        "ui-13":   ["13px",   { lineHeight: "20px" }],
        "ui-13_5": ["13.5px", { lineHeight: "20px" }],
      },

      spacing: {
        "0.5": "2px",
        "1":   "4px",
        "1.5": "6px",
        "2":   "8px",
        "2.5": "10px",
        "3":   "12px",
        "3.5": "14px",
        "4":   "16px",
        "5":   "20px",
        "6":   "24px",
        "7":   "28px",
        "8":   "32px",
        "9":   "36px",
        "10":  "40px",
        "11":  "44px",
        "12":  "48px",
        "14":  "56px",
        "16":  "64px",
        "18":  "72px",
        "20":  "80px",
        "24":  "96px",
        "28":  "112px",
        "32":  "128px",
      },

      borderRadius: {
        none:    "0",
        xs:      "4px",
        sm:      "var(--cs-radius-sm)",
        DEFAULT: "var(--cs-radius-control)",
        control: "var(--cs-radius-control)",
        md:      "var(--cs-radius-md)",
        card:    "var(--cs-radius-card)",
        lg:      "var(--cs-radius-lg)",
        panel:   "var(--cs-radius-panel)",
        xl:      "var(--cs-radius-xl)",
        "2xl":   "20px",
        "3xl":   "28px",
        full:    "9999px",
      },

      boxShadow: {
        xs:      "var(--cs-shadow-xs)",
        sm:      "var(--cs-shadow-sm)",
        DEFAULT: "var(--cs-shadow-sm)",
        md:      "var(--cs-shadow-md)",
        lg:      "var(--cs-shadow-lg)",
        xl:      "var(--cs-shadow-xl)",
        brand:   "var(--cs-shadow-brand)",
        // Legacy direct values kept for any existing usages
        "xs-hard": "0 1px 2px rgba(0,0,0,0.05)",
        agent:     "0 4px 12px rgba(91, 94, 244, 0.15)",
      },

      transitionProperty: {
        "interaction": "background, border-color, color, box-shadow",
        "transform":   "transform",
      },

      transitionDuration: {
        fast:   "120ms",
        normal: "200ms",
        slow:   "300ms",
      },

      animation: {
        "pulse-slow":      "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-in":         "fadeIn 0.2s ease-out",
        "slide-up":        "slideUp 0.3s ease-out",
        "slide-in-right":  "slideInRight 0.3s ease-out",
        "bounce-subtle":   "bounceSlight 0.6s ease-out",
        "shimmer":         "shimmer 1.5s infinite",
        "accordion-down":  "accordion-down 0.2s ease-out",
        "accordion-up":    "accordion-up 0.2s ease-out",
      },

      keyframes: {
        fadeIn: {
          "0%":   { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%":   { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideInRight: {
          "0%":   { opacity: "0", transform: "translateX(16px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
        bounceSlight: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%":      { transform: "translateY(-4px)" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        "accordion-down": {
          from: { height: "0" },
          to:   { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to:   { height: "0" },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;

/** @type {import('tailwindcss').Config} */
export default {
  // Disable Preflight reset to prevent style collisions with Ant Design components
  corePlugins: {
    preflight: false,
  },
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Maps font variables to Tailwind utilities with fallback stacks
        sans: ["var(--font-inter)", "ui-sans-serif", "system-ui", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        display: ["var(--font-poppins)", "sans-serif"],
        mono: ["var(--font-roboto-mono)", "ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"],
        poppins: ["var(--font-poppins)", "sans-serif"],
        roboto: ["var(--font-roboto)", "sans-serif"],
        geist: ["var(--font-geist-sans)", "sans-serif"],
        "geist-mono": ["var(--font-geist-mono)", "monospace"],
      },
      colors: {
        // AIEMS Brand Token Palette
        primary: {
          DEFAULT: "var(--color-primary, #009444)",
          hover: "var(--color-primary-hover, #007a36)",
          light: "rgba(0, 148, 68, 0.1)",
        },
        secondary: {
          DEFAULT: "var(--color-secondary, #0e0e54)",
          hover: "var(--color-secondary-hover, #0a0a40)",
          light: "rgba(14, 14, 84, 0.05)",
        },
        accent: {
          DEFAULT: "var(--color-accent, #58bec6)",
          hover: "var(--color-accent-hover, #2f8389)",
        },
        background: "var(--color-background, #F8FAFC)",
        surface: "#F8FAFC",
        grey: "var(--color-grey, #efefeff0)",
      },
      boxShadow: {
        'glow-primary': '0 0 25px rgba(0, 148, 68, 0.25)',
        'glow-secondary': '0 0 25px rgba(14, 14, 84, 0.3)',
        'ultra': '0 20px 40px -15px rgba(14, 14, 84, 0.12)',
      },
      container: {
        center: true,
        padding: {
          DEFAULT: "1rem",
          sm: "2rem",
          lg: "4rem",
        },
      },
      gridTemplateColumns: {
        layout: "repeat(auto-fit, minmax(250px, 1fr))",
      },
      borderColor: {
        grey: "var(--color-border-grey, #6666)",
      },
      transitionDuration: {
        DEFAULT: "200ms",
      },
      transitionTimingFunction: {
        DEFAULT: "cubic-bezier(0.4, 0, 0.2, 1)",
      },
    },
  },
  plugins: [],
};
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Multi-tonal blacks & dark graphites with subtle depth
        carbon: {
          950: '#070709', // Deepest abyss background
          900: '#0f1013', // Header / Main body
          850: '#141519', // Section containers
          800: '#1a1b21', // Primary cards & message containers
          750: '#21222a', // Nested containers & elevated blocks
          700: '#282a34', // Active tabs, pills & badges
          650: '#323440', // Hover states & button borders
          600: '#3f4150', // Subtle high-contrast dividers
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'Monaco', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.2s ease-out forwards',
        'slide-up': 'slideUp 0.25s ease-out forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}

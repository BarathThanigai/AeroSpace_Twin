/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        critical: '#FF6B6B',
        warning: '#FFA500',
        healthy: '#4CAF50',
        dark: '#1a1a1a',
      }
    },
  },
  plugins: [],
}

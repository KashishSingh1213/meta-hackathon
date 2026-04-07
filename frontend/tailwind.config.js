/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: '#0f172a',
        darker: '#0a0f1f',
        medical: '#1e3a8a',
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
      },
      fontFamily: {
        sans: ['system-ui', 'sans-serif'],
      },
    },
  },
  safelist: [
    'bg-green-500/20',
    'text-green-400',
    'border-green-500/30',
    'bg-yellow-500/20',
    'text-yellow-400',
    'border-yellow-500/30',
    'bg-red-500/20',
    'text-red-400',
    'border-red-500/30',
    'bg-purple-500/20',
    'text-purple-400',
    'border-purple-500/30',
  ],
  plugins: [],
}

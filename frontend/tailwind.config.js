module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#007AFF',
        secondary: '#5AC8FA',
        background: '#0F1419',
        surface: '#1A1F2E',
        text: '#E8EAED',
        text_secondary: '#9AA0A6',
        error: '#FF453A',
        success: '#34C759',
        warning: '#FF9500',
      },
      fontFamily: {
        mono: ['Fira Code', 'Monaco', 'monospace'],
      },
    },
  },
  plugins: [],
}

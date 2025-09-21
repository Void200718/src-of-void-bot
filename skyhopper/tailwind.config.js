import forms from '@tailwindcss/forms'
import typography from '@tailwindcss/typography'
import aspectRatio from '@tailwindcss/aspect-ratio'
import containerQueries from '@tailwindcss/container-queries'
import daisyui from 'daisyui'

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx,js,jsx}'],
  theme: {
    extend: {
      boxShadow: {
        'xl-soft': '0 25px 50px -12px rgba(0, 0, 0, 0.3)',
      },
    },
  },
  plugins: [forms(), typography(), aspectRatio(), containerQueries(), daisyui],
  daisyui: {
    themes: [
      {
        skyhopper: {
          primary: '#0057FF',
          'primary-content': '#E6F0FF',
          secondary: '#00D1B2',
          accent: '#FFC300',
          neutral: '#1F2937',
          'base-100': '#0B1020',
          'base-200': '#0F1426',
          'base-300': '#151A2E',
          info: '#60A5FA',
          success: '#34D399',
          warning: '#FBBF24',
          error: '#F87171',
        },
      },
      'corporate',
      'business',
      'emerald',
      'night',
    ],
    darkTheme: 'night',
  },
}


import { useEffect, useState } from 'react'
import { MoonStar, SunMedium } from 'lucide-react'

const THEMES = ['skyhopper', 'night'] as const
type Theme = typeof THEMES[number]

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(() => (localStorage.getItem('theme') as Theme) || 'skyhopper')

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  return (
    <div className="fixed bottom-5 right-5 z-50">
      <button
        className="btn btn-circle btn-primary shadow-xl"
        onClick={() => setTheme((prev) => (prev === 'night' ? 'skyhopper' : 'night'))}
        aria-label="Toggle theme"
      >
        {theme === 'night' ? <SunMedium /> : <MoonStar />}
      </button>
    </div>
  )
}


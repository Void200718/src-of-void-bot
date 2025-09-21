import { Outlet } from 'react-router-dom'
import { ThemeToggle } from './components/ThemeToggle'
import { Navbar } from './components/Navbar'
import { Footer } from './components/Footer'

function App() {
  return (
    <div className="min-h-screen flex flex-col" data-testid="app-root">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
      <ThemeToggle />
    </div>
  )
}

export default App

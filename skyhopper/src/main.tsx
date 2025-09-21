import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { FlightsPage } from './pages/FlightsPage'
import { BookingPage } from './pages/BookingPage'
import { ConfirmationPage } from './pages/ConfirmationPage'
import { EasterEggPortal } from './game/EasterEggPortal'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <FlightsPage /> },
      { path: 'book/:flightId', element: <BookingPage /> },
      { path: 'confirmation/:bookingId', element: <ConfirmationPage /> },
    ],
  },
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
    <EasterEggPortal />
  </StrictMode>,
)

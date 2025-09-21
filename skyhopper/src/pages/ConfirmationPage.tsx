import { useMemo } from 'react'
import { useParams, Link } from 'react-router-dom'

export function ConfirmationPage() {
  const { bookingId } = useParams()
  const booking = useMemo(() => {
    const all = JSON.parse(localStorage.getItem('bookings') || '[]')
    return all.find((b: any) => b.id === bookingId)
  }, [bookingId])

  if (!booking) {
    return <div className="container mx-auto px-4 py-10"><div className="alert alert-error">Booking not found.</div></div>
  }

  return (
    <div className="container mx-auto px-4 py-10 max-w-3xl">
      <div className="card glass">
        <div className="card-body">
          <h2 className="card-title">Booking confirmed</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <div className="font-semibold">Passenger</div>
              <div>{booking.passenger.name}</div>
              <div className="opacity-70 text-sm">{booking.passenger.email}</div>
            </div>
            <div>
              <div className="font-semibold">Flight</div>
              <div>{booking.flight.airline} — {booking.flight.flightNumber}</div>
              <div className="text-sm opacity-80">{booking.flight.from.city} ({booking.flight.from.airport}) → {booking.flight.to.city} ({booking.flight.to.airport})</div>
            </div>
          </div>
          <div className="divider" />
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div>
              <div className="font-semibold">Departure</div>
              <div>{new Date(booking.flight.departure).toLocaleString()}</div>
            </div>
            <div>
              <div className="font-semibold">Arrival</div>
              <div>{new Date(booking.flight.arrival).toLocaleString()}</div>
            </div>
          </div>
          <div className="divider" />
          <div className="text-right">
            <div className="opacity-80 text-sm">Booking reference</div>
            <div className="font-mono text-xl">{booking.id}</div>
          </div>
          <div className="card-actions justify-end">
            <Link className="btn" to="/">Find more flights</Link>
          </div>
        </div>
      </div>
    </div>
  )
}


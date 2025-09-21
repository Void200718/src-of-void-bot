import { useMemo, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { flights, classMultipliers, meals } from '../seed/flights'
import { z } from 'zod'
import { nanoid } from 'nanoid'

const bookingSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  className: z.enum(['Economy', 'Premium Economy', 'Business', 'First Class']),
  meal: z.enum(['Vegetarian', 'Non-Vegetarian', 'Vegan', 'Gluten-Free', 'Kosher', 'Halal']),
})

export function BookingPage() {
  const { flightId } = useParams()
  const navigate = useNavigate()
  const flight = useMemo(() => flights.find((f) => f.id === flightId), [flightId])

  const [form, setForm] = useState({ name: '', email: '', className: 'Economy' as const, meal: 'Vegetarian' as const })
  const [errors, setErrors] = useState<Record<string, string>>({})

  if (!flight) {
    return <div className="container mx-auto px-4 py-10"><div className="alert alert-error">Flight not found.</div></div>
  }

  const f = flight as NonNullable<typeof flight>
  const base = f.basePrice
  const classMultiplier = classMultipliers[form.className]
  const mealPrice = meals[form.meal]
  const subtotal = base * classMultiplier + mealPrice
  const taxes = Math.round(subtotal * 0.12)
  const total = Math.round(subtotal + taxes)

  function submit() {
    const result = bookingSchema.safeParse(form)
    if (!result.success) {
      const next: Record<string, string> = {}
      for (const issue of result.error.issues) {
        next[issue.path.join('.')] = issue.message
      }
      setErrors(next)
      return
    }

    const bookingId = nanoid(10)
    const payload = { id: bookingId, flightId: f.id, flight: f, passenger: form, pricing: { base, classMultiplier, mealPrice, taxes, total } }
    const existing = JSON.parse(localStorage.getItem('bookings') || '[]')
    existing.push(payload)
    localStorage.setItem('bookings', JSON.stringify(existing))
    navigate(`/confirmation/${bookingId}`)
  }

  return (
    <div className="container mx-auto px-4 py-8 grid lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-4">
        <div className="card glass">
          <div className="card-body">
            <h2 className="card-title">Passenger details</h2>
            <div className="grid md:grid-cols-2 gap-4">
              <label className="form-control">
                <div className="label"><span className="label-text">Full name</span></div>
                <input className={`input input-bordered ${errors.name?'input-error':''}`} value={form.name} onChange={(e)=>setForm((f)=>({...f,name:e.target.value}))} />
                {errors.name && <div className="label"><span className="label-text-alt text-error">{errors.name}</span></div>}
              </label>
              <label className="form-control">
                <div className="label"><span className="label-text">Email</span></div>
                <input className={`input input-bordered ${errors.email?'input-error':''}`} value={form.email} onChange={(e)=>setForm((f)=>({...f,email:e.target.value}))} />
                {errors.email && <div className="label"><span className="label-text-alt text-error">{errors.email}</span></div>}
              </label>
            </div>
          </div>
        </div>

        <div className="card glass">
          <div className="card-body">
            <h2 className="card-title">Preferences</h2>
            <div className="grid md:grid-cols-2 gap-4">
              <label className="form-control">
                <div className="label"><span className="label-text">Travel class</span></div>
                <select className="select select-bordered" value={form.className} onChange={(e)=>setForm((f)=>({...f,className:e.target.value as any}))}>
                  {(['Economy','Premium Economy','Business','First Class'] as const).map((c)=> <option key={c} value={c}>{c}</option>)}
                </select>
              </label>
              <label className="form-control">
                <div className="label"><span className="label-text">Meal preference</span></div>
                <select className="select select-bordered" value={form.meal} onChange={(e)=>setForm((f)=>({...f,meal:e.target.value as any}))}>
                  {Object.keys(meals).map((m)=> <option key={m} value={m}>{m}</option>)}
                </select>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <div className="card glass">
          <div className="card-body">
            <h2 className="card-title">Your flight</h2>
            <div className="text-sm opacity-80">{f.airline} — {f.flightNumber}</div>
            <div className="text-sm">{f.from.city} ({f.from.airport}) → {f.to.city} ({f.to.airport})</div>
            <div className="grid grid-cols-2 gap-2 text-sm mt-2">
              <div>
                <div className="font-semibold">Departure</div>
                <div>{new Date(f.departure).toLocaleString()}</div>
              </div>
              <div>
                <div className="font-semibold">Arrival</div>
                <div>{new Date(f.arrival).toLocaleString()}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="card glass">
          <div className="card-body">
            <h2 className="card-title">Price breakdown</h2>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span>Base fare</span><span>${base.toFixed(0)}</span></div>
              <div className="flex justify-between"><span>Class multiplier ({form.className})</span><span>× {classMultiplier.toFixed(2)}</span></div>
              <div className="flex justify-between"><span>Meal ({form.meal})</span><span>${mealPrice.toFixed(0)}</span></div>
              <div className="flex justify-between"><span>Taxes & fees (12%)</span><span>${taxes.toFixed(0)}</span></div>
              <div className="divider my-2" />
              <div className="flex justify-between font-extrabold text-lg"><span>Total</span><span>${total.toFixed(0)}</span></div>
            </div>
            <button className="btn btn-primary btn-block mt-4" onClick={submit}>Confirm booking</button>
          </div>
        </div>
      </div>
    </div>
  )
}


import { useMemo, useState } from 'react'
import { flights } from '../seed/flights'
import { Link } from 'react-router-dom'
import Fuse from 'fuse.js'
import { ArrowRightLeft, BadgePercent, Shuffle, Timer } from 'lucide-react'
import { motion } from 'framer-motion'

export function FlightsPage() {
  const [query, setQuery] = useState('')
  const [airline, setAirline] = useState('')
  const [origin, setOrigin] = useState('')
  const [destination, setDestination] = useState('')
  const [sortBy, setSortBy] = useState<'price' | 'duration' | 'departure'>('price')

  const fuse = useMemo(() => new Fuse(flights, { keys: ['flightNumber', 'airline', 'from.city', 'to.city', 'from.airport', 'to.airport'], threshold: 0.3 }), [])

  const results = useMemo(() => {
    let list = query ? fuse.search(query).map((r) => r.item) : flights
    if (airline) list = list.filter((f) => f.airline === airline)
    if (origin) list = list.filter((f) => f.from.city === origin || f.from.airport === origin)
    if (destination) list = list.filter((f) => f.to.city === destination || f.to.airport === destination)
    if (sortBy === 'price') list = [...list].sort((a, b) => a.basePrice - b.basePrice)
    if (sortBy === 'duration') list = [...list].sort((a, b) => a.durationMinutes - b.durationMinutes)
    if (sortBy === 'departure') list = [...list].sort((a, b) => new Date(a.departure).getTime() - new Date(b.departure).getTime())
    return list
  }, [query, airline, origin, destination, sortBy, fuse])

  const airlines = useMemo(() => Array.from(new Set(flights.map((f) => f.airline))), [])
  const cities = useMemo(() => Array.from(new Set([...flights.map((f) => f.from.city), ...flights.map((f) => f.to.city)])), [])

  const randomFlight = useMemo(() => flights[Math.floor(Math.random() * flights.length)], [])

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.div initial={{opacity:0, y:20}} animate={{opacity:1,y:0}} transition={{duration:0.6}}
        className="hero min-h-[40vh] rounded-3xl glass overflow-hidden relative">
        <div className="hero-overlay bg-gradient-to-tr from-primary/20 to-base-100/0" />
        <div className="hero-content text-center">
          <div className="max-w-2xl">
            <h1 className="text-5xl font-extrabold tracking-tight">Fly smarter with Skyhopper</h1>
            <p className="py-6 opacity-80">Search, compare, and book curated flights with transparent pricing and premium UX.</p>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <input className="input input-bordered" placeholder="Search cities, airlines, flight no." value={query} onChange={(e) => setQuery(e.target.value)} />
              <select className="select select-bordered" value={airline} onChange={(e) => setAirline(e.target.value)}>
                <option value="">All airlines</option>
                {airlines.map((a) => (
                  <option key={a} value={a}>{a}</option>
                ))}
              </select>
              <select className="select select-bordered" value={origin} onChange={(e) => setOrigin(e.target.value)}>
                <option value="">Any origin</option>
                {cities.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
              <select className="select select-bordered" value={destination} onChange={(e) => setDestination(e.target.value)}>
                <option value="">Any destination</option>
                {cities.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
            <div className="mt-4 flex flex-wrap gap-3 justify-center">
              <div className="join">
                <button className={`btn join-item ${sortBy==='price'?'btn-primary':''}`} onClick={() => setSortBy('price')}><BadgePercent className="mr-2" size={18}/>Price</button>
                <button className={`btn join-item ${sortBy==='duration'?'btn-primary':''}`} onClick={() => setSortBy('duration')}><Timer className="mr-2" size={18}/>Duration</button>
                <button className={`btn join-item ${sortBy==='departure'?'btn-primary':''}`} onClick={() => setSortBy('departure')}><ArrowRightLeft className="mr-2" size={18}/>Departure</button>
              </div>
              <Link className="btn btn-ghost" to={`/book/${randomFlight.id}`}><Shuffle className="mr-2" size={18}/>Surprise me</Link>
            </div>
          </div>
        </div>
      </motion.div>

      <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
        {results.map((f, i) => (
          <motion.div key={f.id} initial={{opacity:0, y:20}} animate={{opacity:1,y:0}} transition={{delay:0.05*i}}
            className="card glass shadow-xl-soft">
            <div className="card-body">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="card-title">{f.airline} — {f.flightNumber}</h2>
                  <p className="opacity-80 text-sm">{f.from.city} ({f.from.airport}) → {f.to.city} ({f.to.airport})</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-extrabold">${f.basePrice.toFixed(0)}</div>
                  <div className="text-xs opacity-70">from</div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-2 text-sm">
                <div>
                  <div className="font-semibold">Departs</div>
                  <div>{new Date(f.departure).toLocaleString()}</div>
                </div>
                <div>
                  <div className="font-semibold">Arrives</div>
                  <div>{new Date(f.arrival).toLocaleString()}</div>
                </div>
                <div>
                  <div className="font-semibold">Duration</div>
                  <div>{Math.floor(f.durationMinutes/60)}h {f.durationMinutes%60}m</div>
                </div>
              </div>
              <div className="card-actions justify-end mt-2">
                <Link to={`/book/${f.id}`} className="btn btn-primary">Book</Link>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}


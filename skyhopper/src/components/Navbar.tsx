import { Link } from 'react-router-dom'
import { Plane, Search } from 'lucide-react'

export function Navbar() {
  return (
    <div className="navbar bg-base-100/80 backdrop-blur-xl sticky top-0 z-50 border-b border-base-300/50">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost text-xl font-black tracking-wider">
          <Plane className="mr-2 text-primary" size={22} /> Skyhopper
        </Link>
      </div>
      <div className="flex-none gap-2">
        <div className="form-control hidden md:block">
          <input type="text" placeholder="Search flights" className="input input-bordered w-64" aria-label="Search" />
        </div>
        <button className="btn btn-ghost btn-circle md:hidden" aria-label="Search">
          <Search />
        </button>
      </div>
    </div>
  )
}


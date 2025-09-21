export type Flight = {
  id: string
  flightNumber: string
  airline: string
  from: { city: string; airport: string }
  to: { city: string; airport: string }
  departure: string
  arrival: string
  durationMinutes: number
  basePrice: number
}

const now = new Date()

function addHours(base: Date, hours: number) {
  return new Date(base.getTime() + hours * 3600 * 1000)
}

function mk(
  id: string,
  flightNumber: string,
  airline: string,
  from: [string, string],
  to: [string, string],
  departInHours: number,
  durationHrs: number,
  basePrice: number,
): Flight {
  const departure = addHours(now, departInHours)
  const arrival = addHours(departure, durationHrs)
  return {
    id,
    flightNumber,
    airline,
    from: { city: from[0], airport: from[1] },
    to: { city: to[0], airport: to[1] },
    departure: departure.toISOString(),
    arrival: arrival.toISOString(),
    durationMinutes: durationHrs * 60,
    basePrice,
  }
}

export const flights: Flight[] = [
  mk('f1', 'SH101', 'Skyhopper Airways', ['New York', 'JFK'], ['Los Angeles', 'LAX'], 24, 6, 320),
  mk('f2', 'SH202', 'Skyhopper Airways', ['Los Angeles', 'LAX'], ['Chicago', 'ORD'], 28, 4, 220),
  mk('f3', 'SH303', 'Skyhopper Airways', ['Chicago', 'ORD'], ['Miami', 'MIA'], 30, 3, 180),
  mk('f4', 'SH404', 'Skyhopper Airways', ['Miami', 'MIA'], ['New York', 'JFK'], 36, 3, 190),
  mk('f5', 'NX500', 'NeonX Air', ['San Francisco', 'SFO'], ['Tokyo', 'HND'], 48, 11, 780),
  mk('f6', 'NX510', 'NeonX Air', ['Tokyo', 'HND'], ['San Francisco', 'SFO'], 60, 10, 760),
  mk('f7', 'AE111', 'AeroExpress', ['London', 'LHR'], ['Paris', 'CDG'], 20, 1, 140),
  mk('f8', 'AE112', 'AeroExpress', ['Paris', 'CDG'], ['Rome', 'FCO'], 26, 2, 160),
  mk('f9', 'AE113', 'AeroExpress', ['Rome', 'FCO'], ['Madrid', 'MAD'], 34, 2, 170),
  mk('f10', 'BL700', 'BlueLagoon Air', ['Sydney', 'SYD'], ['Melbourne', 'MEL'], 18, 1, 120),
  mk('f11', 'BL701', 'BlueLagoon Air', ['Melbourne', 'MEL'], ['Brisbane', 'BNE'], 22, 2, 140),
  mk('f12', 'BL702', 'BlueLagoon Air', ['Brisbane', 'BNE'], ['Perth', 'PER'], 40, 5, 260),
  mk('f13', 'OR210', 'Orion Air', ['Dubai', 'DXB'], ['Singapore', 'SIN'], 44, 7, 520),
  mk('f14', 'OR211', 'Orion Air', ['Singapore', 'SIN'], ['Bangkok', 'BKK'], 52, 2, 210),
  mk('f15', 'OR212', 'Orion Air', ['Bangkok', 'BKK'], ['Hong Kong', 'HKG'], 58, 3, 240),
  mk('f16', 'PA900', 'Polar Aurora', ['Reykjavik', 'KEF'], ['New York', 'JFK'], 62, 6, 350),
  mk('f17', 'PA901', 'Polar Aurora', ['New York', 'JFK'], ['Reykjavik', 'KEF'], 70, 6, 340),
  mk('f18', 'PA902', 'Polar Aurora', ['Reykjavik', 'KEF'], ['London', 'LHR'], 76, 3, 230),
  mk('f19', 'SA120', 'Sahara Air', ['Cairo', 'CAI'], ['Istanbul', 'IST'], 38, 2, 180),
  mk('f20', 'SA121', 'Sahara Air', ['Istanbul', 'IST'], ['Cairo', 'CAI'], 46, 2, 180),
  mk('f21', 'SH777', 'Skyhopper Airways', ['Seattle', 'SEA'], ['Austin', 'AUS'], 54, 4, 210),
  mk('f22', 'NX777', 'NeonX Air', ['Delhi', 'DEL'], ['Dubai', 'DXB'], 82, 3, 260),
]

export const classMultipliers = {
  'Economy': 1,
  'Premium Economy': 1.35,
  'Business': 2.2,
  'First Class': 3.1,
} as const

export const meals: Record<string, number> = {
  'Vegetarian': 0,
  'Non-Vegetarian': 10,
  'Vegan': 8,
  'Gluten-Free': 6,
  'Kosher': 12,
  'Halal': 10,
}


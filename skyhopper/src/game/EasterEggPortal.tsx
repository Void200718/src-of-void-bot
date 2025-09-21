import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'

const QUESTIONS = [
  { q: 'Which city is known as the City of Light?', a: 'Paris' },
  { q: 'Which airport code is LAX?', a: 'Los Angeles' },
  { q: 'Which city has the Colosseum?', a: 'Rome' },
]

export function EasterEggPortal() {
  const [open, setOpen] = useState(false)
  const clicksRef = useRef(0)
  const [index, setIndex] = useState(0)
  const [answer, setAnswer] = useState('')
  const [won, setWon] = useState(false)

  useEffect(() => {
    const logo = document.querySelector('.navbar .btn-ghost')
    if (!logo) return
    const onClick = () => {
      clicksRef.current += 1
      if (clicksRef.current >= 5) setOpen(true)
    }
    logo.addEventListener('click', onClick)
    return () => logo.removeEventListener('click', onClick)
  }, [])

  function submit() {
    if (answer.trim().toLowerCase() === QUESTIONS[index].a.toLowerCase()) {
      if (index + 1 === QUESTIONS.length) {
        setWon(true)
      } else {
        setIndex((i) => i + 1)
        setAnswer('')
      }
    } else {
      alert('Not quite! Try again.')
    }
  }

  if (!open) return null

  return createPortal(
    <div className="fixed inset-0 z-[100] flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={() => setOpen(false)} />
      <div className="card glass w-full max-w-lg relative">
        <div className="card-body">
          <h2 className="card-title">City Trivia — Secret Cabin</h2>
          {!won ? (
            <>
              <p className="opacity-80">Answer correctly to unlock a reward.</p>
              <div className="font-semibold">Q{index + 1}. {QUESTIONS[index].q}</div>
              <input className="input input-bordered" value={answer} onChange={(e)=>setAnswer(e.target.value)} onKeyDown={(e)=> e.key==='Enter' && submit()} />
              <div className="card-actions justify-end">
                <button className="btn" onClick={()=>setOpen(false)}>Close</button>
                <button className="btn btn-primary" onClick={submit}>Submit</button>
              </div>
            </>
          ) : (
            <div className="text-center space-y-3">
              <div className="text-3xl font-extrabold">You unlocked a free upgrade!</div>
              <div className="opacity-80">Use code SKY-SECRET for a complimentary class upgrade on your next booking.</div>
              <button className="btn btn-primary" onClick={()=>setOpen(false)}>Nice!</button>
            </div>
          )}
        </div>
      </div>
    </div>,
    document.body,
  )
}


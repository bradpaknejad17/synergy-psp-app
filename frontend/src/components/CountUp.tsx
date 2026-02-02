"use client"
import React, { useEffect, useRef, useState } from 'react'

export default function CountUp({ value, duration = 400, decimals = 0, className = '' }: { value: number; duration?: number; decimals?: number; className?: string }) {
  const [display, setDisplay] = useState(value)
  const rafRef = useRef<number | null>(null)
  const startRef = useRef<number | null>(null)
  const fromRef = useRef<number>(value)

  useEffect(() => {
    const from = fromRef.current
    const to = value
    const start = performance.now()
    startRef.current = start

    function step(now: number) {
      const elapsed = now - start
      const t = Math.min(1, elapsed / duration)
      const eased = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t // easeInOut quad
      const current = from + (to - from) * eased
      setDisplay(Number(current.toFixed(decimals)))
      if (t < 1) {
        rafRef.current = requestAnimationFrame(step)
      } else {
        fromRef.current = to
      }
    }

    rafRef.current = requestAnimationFrame(step)
    return () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); }
  }, [value, duration, decimals])

  return <span className={className}>{display}</span>
}

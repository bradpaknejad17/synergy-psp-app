"use client"
import React, { useEffect, useState } from 'react'
import OdometerDigit from './OdometerDigit'

type Props = {
  endDate?: string | null
}

function parseToLocalEndOfDay(s?: string | null): number | null {
  if (!s) return null
  // handle date-only YYYY-MM-DD as local end of day
  if (/^\d{4}-\d{2}-\d{2}$/.test(s)) {
    const [y, m, d] = s.split('-').map((n) => Number(n))
    return new Date(y, m - 1, d, 23, 59, 59, 999).getTime()
  }
  const t = Date.parse(s)
  return Number.isNaN(t) ? null : t
}

function pad(n: number) {
  return n.toString().padStart(2, '0')
}

export default function Countdown({ endDate }: Props) {
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(id)
  }, [])

  const targetMs = parseToLocalEndOfDay(endDate)
  if (!targetMs) return null

  const diff = Math.max(0, targetMs - now)
  const msInSec = 1000
  const msInMin = msInSec * 60
  const msInHour = msInMin * 60
  const msInDay = msInHour * 24

  const days = Math.floor(diff / msInDay)
  const hours = Math.floor((diff % msInDay) / msInHour)
  const minutes = Math.floor((diff % msInHour) / msInMin)
  const seconds = Math.floor((diff % msInMin) / msInSec)

  const hoursLeft = diff / msInHour

  // Card-style container with urgency states: last 1 hour -> red, last 24 hours -> amber, otherwise neutral
  let cardBg = 'bg-white'
  let textClass = 'text-[color:var(--muted-text)]'
  let extraClass = 'border border-slate-100'
  let glow = ''

  if (hoursLeft <= 1) {
    cardBg = 'bg-red-50'
    textClass = 'text-red-500'
    glow = 'shadow-[0_0_10px_rgba(239,68,68,0.08)]'
  } else if (hoursLeft <= 24) {
    cardBg = 'bg-amber-50'
    textClass = 'text-amber-600'
  }

  const ariaLabel = `Time remaining ${days} days ${pad(hours)} hours ${pad(minutes)} minutes ${pad(seconds)} seconds`

  const toDigits = (v: number) => String(v).split('')

  return (
    <div role="status" aria-live="polite" aria-label={ariaLabel} className="mt-1">
      <div className={`flex items-center gap-3 ${cardBg} ${extraClass} ${glow} rounded-lg px-4 py-2 shadow-sm`}> 
        <div className="flex items-baseline gap-3">
          {/* Days */}
          <div className="flex items-baseline gap-1">
            {toDigits(days).map((d, i) => (
              <span key={`d-${i}`} className="inline-block overflow-hidden" style={{ height: 20 }}>
                <OdometerDigit char={d} />
              </span>
            ))}
            <span className="text-sm font-normal opacity-60 ml-0.5">d</span>
          </div>

          {/* Hours */}
          <div className="flex items-baseline gap-1">
            {toDigits(Number(pad(hours))).map((d, i) => (
              <span key={`h-${i}`} className="inline-block overflow-hidden" style={{ height: 20 }}>
                <OdometerDigit char={d} />
              </span>
            ))}
            <span className="text-sm font-normal opacity-60 ml-0.5">h</span>
          </div>

          {/* Minutes */}
          <div className="flex items-baseline gap-1">
            {toDigits(Number(pad(minutes))).map((d, i) => (
              <span key={`m-${i}`} className="inline-block overflow-hidden" style={{ height: 20 }}>
                <OdometerDigit char={d} />
              </span>
            ))}
            <span className="text-sm font-normal opacity-60 ml-0.5">m</span>
          </div>

          {/* Seconds (lower opacity) */}
          <div className="flex items-baseline gap-1 opacity-60">
            {toDigits(Number(pad(seconds))).map((d, i) => (
              <span key={`s-${i}`} className="inline-block overflow-hidden" style={{ height: 20 }}>
                <OdometerDigit char={d} isSeconds />
              </span>
            ))}
            <span className="text-sm font-normal ml-0.5 opacity-60">s</span>
          </div>
        </div>
      </div>
    </div>
  )
}

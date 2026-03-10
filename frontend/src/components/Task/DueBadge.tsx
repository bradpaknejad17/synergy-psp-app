"use client"
import React from 'react'

function parseToLocalDate(s: string | undefined | null): Date | null {
  if (!s) return null
  const ymd = /^\d{4}-\d{2}-\d{2}$/.test(s)
  if (ymd) {
    const [y, m, d] = s.split('-').map((n) => Number(n))
    return new Date(y, m - 1, d)
  }
  const t = Date.parse(s)
  return Number.isNaN(t) ? null : new Date(t)
}

export default function DueBadge({ due_date, className = '' }: { due_date?: string | null; className?: string }) {
  let daysRemaining: number | null = null
  if (due_date) {
    const d = parseToLocalDate(due_date)
    if (d) {
      const today = new Date()
      const localToday = new Date(today.getFullYear(), today.getMonth(), today.getDate())
      const msPerDay = 1000 * 60 * 60 * 24
      daysRemaining = Math.ceil((d.getTime() - localToday.getTime()) / msPerDay)
    }
  }

  return (
    <div className={`inline-flex items-center gap-3 px-3 py-1 rounded-full text-xs ${daysRemaining !== null && daysRemaining <= 7 ? 'bg-[color:var(--warning)]/10 text-[color:var(--warning)]' : 'bg-white/60 text-[color:var(--muted-text)]'} ${className}`}>
      <div>{due_date ? ((): string => {
        const d = parseToLocalDate(due_date)
        return d ? d.toLocaleDateString() : '—'
      })() : '—'}</div>
      <div className="text-xs">{daysRemaining === null ? '' : `${daysRemaining}d`}</div>
    </div>
  )
}

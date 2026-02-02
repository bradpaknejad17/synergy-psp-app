"use client"
import React from 'react'
import { useTasksContext } from '../../context/TasksContext'
import CountUp from '../CountUp'

export default function PulseBar({ categories }: { categories: string[] }) {
  const { categoryPercents, totalPercent } = useTasksContext()

  return (
    <div className="grid grid-cols-6 gap-3 w-full">
      {categories.map((c) => {
        const pct = categoryPercents[c] ?? 0
        const isZero = pct === 0
        return (
          <div key={c} className={`p-3 rounded-md bg-slate-50 shadow transform hover:shadow-lg hover:-translate-y-1 transition ease-out duration-150 flex flex-col justify-center ${isZero ? 'text-slate-400' : 'text-slate-900'}`}>
            <div className="text-xs text-[color:var(--muted-text)]">{c}</div>
            <div className="mt-1 text-lg font-semibold font-mono font-tnum">
              <CountUp value={pct} className="inline-block" />%
            </div>
            <div className="mt-2 h-1 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-[color:var(--accent)]" style={{ width: `${pct}%` }} />
            </div>
          </div>
        )
      })}
      <div className="p-3 rounded-md bg-slate-50 shadow transform hover:shadow-lg hover:-translate-y-1 transition ease-out duration-150 flex items-center justify-center">
        <div className="text-sm text-slate-700">
          <div className="text-xs text-[color:var(--muted-text)]">Total</div>
          <div className="text-xl font-mono font-tnum font-semibold"><CountUp value={totalPercent} />%</div>
        </div>
      </div>
    </div>
  )
}

"use client"
import React from 'react'
import CompletedBadge from './CompletedBadge'
import TaskTitle from './TaskTitle'
import MetricPair from './MetricPair'
import DueBadge from './DueBadge'

export default function TaskRow({ task, onOpenEdit }: { task: any; onOpenEdit?: (task: any) => void }) {
  const percent = Math.min(100, Math.round((task.currentValue / Math.max(1, task.targetValue)) * 100))

  const curNumTop = Number(task.currentValue || 0)
  const tgtNumTop = Number(task.targetValue || 0)
  const completed = curNumTop >= tgtNumTop

  // due date warning
  let daysRemaining: number | null = null
  if (task.dueDate) {
    // Parse backend date strings like 'YYYY-MM-DD' as local dates (avoid UTC shift)
    const parseToLocalDate = (s: string | undefined | null): Date | null => {
      if (!s) return null
      const ymd = /^\d{4}-\d{2}-\d{2}$/.test(s)
      if (ymd) {
        const [y, m, d] = s.split('-').map((n) => Number(n))
        return new Date(y, m - 1, d)
      }
      const t = Date.parse(s)
      return Number.isNaN(t) ? null : new Date(t)
    }

    const d = parseToLocalDate(task.dueDate)
    if (d) {
      const today = new Date()
      const localToday = new Date(today.getFullYear(), today.getMonth(), today.getDate())
      const msPerDay = 1000 * 60 * 60 * 24
      daysRemaining = Math.ceil((d.getTime() - localToday.getTime()) / msPerDay)
    }
  }

  return (
    <div className="relative rounded-md overflow-hidden border border-slate-100 hover:border-slate-200">
      <div className="absolute inset-0" style={{ pointerEvents: 'none' }}>
        <div className="absolute left-0 top-0 bottom-0 rounded-sm" style={{ width: `${percent}%`, background: 'linear-gradient(90deg, rgba(99,102,241,0.12) 0%, rgba(99,102,241,0.06) 100%)' }} />
      </div>
      <div onClick={() => onOpenEdit?.(task)} className="relative grid grid-cols-12 items-center gap-4 py-4 px-3 hover:bg-slate-50 rounded-sm h-auto cursor-pointer" role="listitem">
        <div className="col-span-7 min-w-0 max-w-[60%]">
          <TaskTitle title={task.title} metricName={task.metricName} />
        </div>

        <div className="col-span-3 flex items-center justify-end">
          <div className="flex items-baseline gap-1 whitespace-nowrap">
            <MetricPair currentValue={task.currentValue} targetValue={task.targetValue} unit={task.unit} />
          </div>
        </div>

        <div className="col-span-2 flex justify-end pl-6">
          {completed ? (
            <CompletedBadge />
            ) : (
            <DueBadge dueDate={task.dueDate} />
          )}
        </div>
      </div>
    </div>
  )
}

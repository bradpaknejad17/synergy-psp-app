"use client"
import React, { createContext, useContext, useState } from 'react'
import { patchTask } from '../lib/api'

export interface Task {
  id: string
  category: string
  title: string
  metricName?: string
  currentValue: number
  targetValue: number
  unit?: string
  dueDate?: string | null
}

export interface PSP {
  id?: string | number
  title?: string
  start_date?: string
  end_date?: string
  [k: string]: any
}

export type Metrics = {
  categoryPercents: Record<string, number>
  totalPercent: number
}

type PSPState = {
  tasks: Task[]
  updateTask: (id: string, patch: Partial<Task>) => Promise<void>
  createTask: (task: Partial<Task>) => Promise<void>
  categoryPercents: Record<string, number>
  totalPercent: number
  psp?: PSP
}

const PSPContext = createContext<PSPState | undefined>(undefined)

export function PSPProvider({ children, initialTasks = [], psp }: { children: React.ReactNode; initialTasks?: Task[]; psp?: PSP }) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks)
  const [categoryPercents, setCategoryPercents] = useState<Record<string, number>>({})
  const [totalPercent, setTotalPercent] = useState<number>(0)

  async function updateTask(id: string, patch: Partial<Task>) {
    const prev = tasks.find((t) => t.id === id)
    if (!prev) return

    if (patch.dueDate && psp) {
      const d = new Date(patch.dueDate)
      const start = new Date((psp as any).start_date || (psp as any).startDate)
      const end = new Date((psp as any).end_date || (psp as any).endDate)
      if (d < start || d > end) {
        throw new Error('dueDate_out_of_range')
      }
    }

    setTasks((cur) => cur.map((t) => (t.id === id ? { ...t, ...patch } : t)))

    try {
      const server = await patchTask(id, patch)
      setTasks((cur) => cur.map((t) => (t.id === id ? { ...t, ...server } : t)))
      computeAggregates()
    } catch (err) {
      setTasks((cur) => cur.map((t) => (t.id === id ? (prev as Task) : t)))
      console.error('Failed to update task', err)
      throw err
    }
  }

  async function createTask(task: Partial<Task>) {
    const id = `temp-${Math.random().toString(36).slice(2, 9)}`
    const newTask: Task = { id, category: task.category || 'General', title: task.title || 'New Task', currentValue: task.currentValue || 0, targetValue: task.targetValue || 1, unit: task.unit || '', dueDate: task.dueDate || null }
    setTasks((cur) => [newTask, ...cur])

    try {
      const pspId = (psp as any)?.id ?? (psp as any)?.psp_id ?? null
      if (!pspId) throw new Error('psp_id_missing')
      const server = await import('../lib/api').then((m) => m.createTask(pspId, task))
      setTasks((cur) => cur.map((t) => (t.id === id ? { ...t, ...server, id: String((server as any).id) } : t)))
      computeAggregates()
    } catch (err) {
      setTasks((cur) => cur.filter((t) => t.id !== id))
      console.error('Failed to create task', err)
      throw err
    }
  }

  function computeAggregates() {
    const byCat: Record<string, { totalPct: number; count: number }> = {}
    let totalPctSum = 0
    let totalCount = 0

    tasks.forEach((t) => {
      const cat = t.category || 'Uncategorized'
      const cur = Number(t.currentValue || 0)
      const tgt = Number(t.targetValue || 0)
      const rawPct = tgt <= 0 ? 0 : Math.round((cur / tgt) * 100)
      const pct = Math.min(100, rawPct)
      if (!byCat[cat]) byCat[cat] = { totalPct: 0, count: 0 }
      byCat[cat].totalPct += pct
      byCat[cat].count += 1
      totalPctSum += pct
      totalCount += 1
    })

    const catPercents: Record<string, number> = {}
    Object.keys(byCat).forEach((c) => {
      const { totalPct, count } = byCat[c]
      catPercents[c] = count === 0 ? 0 : Math.round(totalPct / count)
    })

    setCategoryPercents(catPercents)
    setTotalPercent(totalCount === 0 ? 0 : Math.round(totalPctSum / totalCount))
  }

  React.useEffect(() => { computeAggregates() }, [tasks])

  return <PSPContext.Provider value={{ tasks, updateTask, createTask, categoryPercents, totalPercent, psp }}>{children}</PSPContext.Provider>
}

export function usePSP() {
  const ctx = useContext(PSPContext)
  if (!ctx) throw new Error('usePSP must be used within PSPProvider')
  return ctx
}

// Backwards-compatible exports
export const TasksProvider = PSPProvider
export function useTasksContext() { return usePSP() }

export type PSPContextState = ReturnType<typeof usePSP>

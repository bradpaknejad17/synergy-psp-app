"use client"
import React from 'react'
import { motion } from 'framer-motion'
import H1Vision from './Header/H1Vision'
import PulseBar from './Pulse/PulseBar'
import CategorySection from './Board/CategorySection'
import { TasksProvider } from '../context/TasksContext'
import { usePSP } from '../hooks/usePSP'
import { CATEGORIES } from '../constants/categories'

export default function PSPSingleView({ pspId }: { pspId: string }) {
  const { psp, loading } = usePSP(pspId)
  const categories = CATEGORIES

  if (loading) return <div className="p-8">Loading PSP…</div>
  if (!psp) return <div className="p-8 text-red-500">PSP not found</div>

  const initialTasks = (psp.tasks || []).map((t: any) => ({
    id: String(t.id),
    category: t.category,
    description: t.description || '',
    start_date: t.start_date,
    completed_value: t.completed_value ?? 0,
    target_value: t.target_value ?? 0,
    unit: t.unit,
    due_date: t.due_date,
    completed: Boolean(t.completed),
  }))

  return (
    <TasksProvider initialTasks={initialTasks} psp={psp}>
      <main className="max-w-6xl mx-auto p-8">
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <H1Vision psp={psp} />
          <div className="mt-6">
            <PulseBar categories={categories} />
          </div>
          <div className="mt-8 space-y-6">
            {categories.map((c) => (
              <CategorySection key={c} name={c} />
            ))}
          </div>
        </motion.div>
      </main>
    </TasksProvider>
  )
}

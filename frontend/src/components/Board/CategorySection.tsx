"use client"
import React, { useState } from 'react'
import { useTasksContext } from '../../context/TasksContext'
import AddTaskModal from '../Task/AddTaskModal'
import CategoryHeader from './CategoryHeader'
import CategoryTasks from './CategoryTasks'

export default function CategorySection({ name }: { name: string }) {
  const { tasks, createTask, updateTask } = useTasksContext()
  const categoryTasks = tasks.filter((t) => t.category === name)
  // sort: incomplete tasks first, then by due date ascending within each group
  const sortedTasks = [...categoryTasks].sort((a, b) => {
    const aCur = Number(a.currentValue || 0)
    const aTgt = Number(a.targetValue || 0)
    const bCur = Number(b.currentValue || 0)
    const bTgt = Number(b.targetValue || 0)
    const aCompleted = aCur >= aTgt
    const bCompleted = bCur >= bTgt
    if (aCompleted !== bCompleted) return aCompleted ? 1 : -1

    // both same completion status -> sort by due date ascending (earlier first)
    const parseToLocalMillis = (s: string | undefined | null) => {
      if (!s) return Infinity
      if (/^\d{4}-\d{2}-\d{2}$/.test(s)) {
        const [y, m, d] = s.split('-').map((n) => Number(n))
        return new Date(y, m - 1, d).getTime()
      }
      const t = Date.parse(s)
      return Number.isNaN(t) ? Infinity : t
    }

    const aDue = parseToLocalMillis(a.dueDate)
    const bDue = parseToLocalMillis(b.dueDate)
    if (aDue === bDue) return 0
    return aDue < bDue ? -1 : 1
  })
  const [collapsed, setCollapsed] = useState(false)
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingTask, setEditingTask] = useState<any | null>(null)

  const containerId = `category-${name.replace(/\s+/g, '-')}-tasks`

  return (
    <section className="bg-[color:var(--surface)] p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-150">
      <CategoryHeader name={name} count={categoryTasks.length} collapsed={collapsed} onToggle={() => setCollapsed((v) => !v)} onAdd={() => { setEditingTask(null); setShowAddModal(true) }} />

      <CategoryTasks name={name} sortedTasks={sortedTasks} collapsed={collapsed} containerId={containerId} onEdit={(task) => { setEditingTask(task); setShowAddModal(true) }} />

      {showAddModal && (
        <AddTaskModal
          category={name}
          task={editingTask ?? undefined}
          onClose={() => { setShowAddModal(false); setEditingTask(null) }}
          onCreate={async (payload) => await createTask(payload)}
          onUpdate={async (id, patch) => await updateTask(id, patch)}
        />
      )}
    </section>
  )
}

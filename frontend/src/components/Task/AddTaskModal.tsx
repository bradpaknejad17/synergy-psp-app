"use client"
import React, { useEffect, useMemo, useState } from 'react'

export default function AddTaskModal({ category, onClose, onCreate, task, onUpdate }: { category?: string; onClose: () => void; onCreate?: (payload: any) => Promise<void>; task?: any; onUpdate?: (id: string, patch: any) => Promise<void> }) {
  const [title, setTitle] = useState('')
  const [currentValue, setCurrentValue] = useState<number | ''>('')
  const [targetValue, setTargetValue] = useState<number | ''>('')
  const [unit, setUnit] = useState('')
  const [dueDate, setDueDate] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    if (!title.trim()) { setError('Please enter a title'); return }
    if (targetValue === '' || Number(targetValue) <= 0) { setError('Please enter a target value'); return }
    const payload = {
      category: task?.category || category,
      title: title.trim(),
      currentValue: Number(currentValue) || 0,
      targetValue: Number(targetValue),
      unit: unit || undefined,
      dueDate: dueDate || undefined
    }
    try {
      setSubmitting(true)
      if (task && onUpdate) {
        // compute changed fields only
        const patch: any = {}
        if (title.trim() !== (task.title || '')) patch.title = title.trim()
        if (Number(currentValue || 0) !== Number(task.currentValue || 0)) patch.currentValue = Number(currentValue || 0)
        if (Number(targetValue || 0) !== Number(task.targetValue || 0)) patch.targetValue = Number(targetValue || 0)
        if ((unit || '') !== (task.unit || '')) patch.unit = unit || ''
        if ((dueDate || null) !== (task.dueDate || null)) patch.dueDate = dueDate || null
        if (Object.keys(patch).length > 0) {
          await onUpdate(task.id, patch)
        }
      } else if (onCreate) {
        await onCreate(payload)
      }
      onClose()
    } catch (e: any) {
      setError(e?.message || 'Failed to create task')
    } finally { setSubmitting(false) }
  }

  // initialize when editing an existing task
  useEffect(() => {
    if (task) {
      setTitle(task.title || '')
      setCurrentValue(task.currentValue ?? '')
      setTargetValue(task.targetValue ?? '')
      setUnit(task.unit || '')
      setDueDate(task.dueDate || null)
    } else {
      setTitle('')
      setCurrentValue('')
      setTargetValue('')
      setUnit('')
      setDueDate(null)
    }
  }, [task])

  const initial = useMemo(() => ({ title: task?.title || '', currentValue: task?.currentValue ?? '', targetValue: task?.targetValue ?? '', unit: task?.unit || '', dueDate: task?.dueDate || null }), [task])
  const dirty = title !== initial.title || String(currentValue) !== String(initial.currentValue) || String(targetValue) !== String(initial.targetValue) || unit !== initial.unit || (dueDate || null) !== (initial.dueDate || null)

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <form onSubmit={handleSubmit} className="relative bg-white dark:bg-[#0f1115] rounded-lg p-6 w-full max-w-md shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-lg font-medium">{task ? 'Edit Task' : 'Add Task'}</h4>
          <button type="button" onClick={onClose} aria-label="Close" className="text-sm text-[color:var(--muted-text)] p-1 rounded hover:bg-gray-100">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 20 20" fill="none" stroke="currentColor">
              <path strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" d="M6 6l8 8M6 14L14 6" />
            </svg>
          </button>
        </div>

        <div className="space-y-3">
          <div>
            <label className="block text-xs text-[color:var(--muted-text)]">Title</label>
            <input autoFocus value={title} onChange={(e) => setTitle(e.target.value)} className="w-full mt-1 p-2 rounded border text-sm" />
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs text-[color:var(--muted-text)]">Current</label>
              <input value={currentValue === '' ? '' : String(currentValue)} onChange={(e) => setCurrentValue(e.target.value === '' ? '' : Number(e.target.value))} type="number" className="w-full mt-1 p-2 rounded border text-sm text-right" />
            </div>
            <div>
              <label className="block text-xs text-[color:var(--muted-text)]">Target</label>
              <input required value={targetValue === '' ? '' : String(targetValue)} onChange={(e) => setTargetValue(e.target.value === '' ? '' : Number(e.target.value))} type="number" className="w-full mt-1 p-2 rounded border text-sm text-right" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs text-[color:var(--muted-text)]">Unit</label>
              <select value={unit} onChange={(e) => setUnit(e.target.value)} className="w-full mt-1 p-2 rounded border text-sm">
                <option value="">(none)</option>
                <option value="count">count</option>
                <option value="lbs">lbs</option>
                <option value="USD">USD</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-[color:var(--muted-text)]">Due date</label>
              <input value={dueDate ?? ''} onChange={(e) => setDueDate(e.target.value || null)} type="date" className="w-full mt-1 p-2 rounded border text-sm" />
            </div>
          </div>
          {error && <div className="text-sm text-red-500">{error}</div>}
        </div>

        <div className="mt-4 flex justify-end gap-2">
          <button type="button" onClick={onClose} className="px-3 py-2 rounded bg-white border">Cancel</button>
          <button
            type="submit"
            disabled={submitting || (task ? !dirty : false)}
            aria-disabled={submitting || (task ? !dirty : false)}
            className="px-4 py-2 rounded bg-[color:var(--accent)] text-white disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {submitting ? (task ? 'Updating...' : 'Creating...') : (task ? 'Update' : 'Create')}
          </button>
        </div>
      </form>
    </div>
  )
}

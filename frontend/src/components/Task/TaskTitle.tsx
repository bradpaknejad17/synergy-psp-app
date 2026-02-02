"use client"
import React from 'react'

export default function TaskTitle({ title, metricName }: { title: string; metricName?: string }) {
  return (
    <>
      <div className="text-sm font-medium whitespace-normal break-words">{title}</div>
      <div className="text-xs text-[color:var(--muted-text)] whitespace-normal break-words">{metricName || ''}</div>
    </>
  )
}

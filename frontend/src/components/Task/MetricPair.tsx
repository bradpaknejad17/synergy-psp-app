"use client"
import React from 'react'
import { formatMetric, formatCompactNumber } from '../../utils/format'

export default function MetricPair({ currentValue, targetValue, unit }: { currentValue?: number; targetValue?: number; unit?: string }) {
  const curNum = Number(currentValue || 0)
  const tgtNum = Number(targetValue || 0)
  const curDisplay = unit && String(unit).toUpperCase() === 'USD' ? formatMetric(curNum, 'USD') : formatCompactNumber(curNum)
  const tgtDisplay = formatCompactNumber(tgtNum, unit)

  return (
    <span className="inline-flex items-baseline">
      <span className="font-bold text-slate-900">{curDisplay}</span>
      <span className="text-slate-400 px-1">/</span>
      <span className="text-sm text-slate-500 font-medium">{tgtDisplay}</span>
    </span>
  )
}

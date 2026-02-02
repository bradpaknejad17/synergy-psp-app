"use client"
import React from 'react'

export default function ContractLabel({ children }: { children: React.ReactNode }) {
  return (
    <div className="text-[10px] uppercase tracking-[0.25em] font-semibold text-slate-500 mb-1">{children}</div>
  )
}

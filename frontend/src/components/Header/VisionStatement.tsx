"use client"
import React from 'react'

export default function VisionStatement({ children }: { children: React.ReactNode }) {
  return (
    <p className="mt-4 text-lg font-light italic text-slate-500 leading-relaxed max-w-4xl pl-6 border-l-2 border-[#700b70]/30">{children}</p>
  )
}

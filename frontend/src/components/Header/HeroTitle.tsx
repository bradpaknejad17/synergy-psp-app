"use client"
import React from 'react'

export default function HeroTitle({ title }: { title: string }) {
  return (
    <h1 className="text-4xl font-extrabold tracking-tighter leading-tight mb-2 text-slate-900">{title}</h1>
  )
}

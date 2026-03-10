"use client"
import React from 'react'

export default function TaskTitle({ description }: { description: string }) {
  return (
    <>
      <div className="text-sm font-medium whitespace-normal break-words">{description}</div>
    </>
  )
}

import '../src/styles/globals.css'
import React from 'react'

export const metadata = {
  title: 'PSP Dashboard',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased bg-[color:var(--bg)] text-[color:var(--text)]">{children}</body>
    </html>
  )
}
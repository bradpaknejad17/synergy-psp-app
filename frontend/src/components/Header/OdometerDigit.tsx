"use client"
import React from 'react'
import { AnimatePresence, motion } from 'framer-motion'

type Props = {
  char: string
  isSeconds?: boolean
  className?: string
}

const spring = { type: 'spring', stiffness: 400, damping: 40 }

function Digit({ char, isSeconds, className = '' }: Props) {
  const isNumber = /^[0-9]$/.test(char)

  if (!isNumber) {
    return (
      <span className={`inline-block ${className} text-sm font-normal opacity-60`}>{char}</span>
    )
  }

  return (
    <span className={`inline-block overflow-hidden align-middle ${className}`} style={{ height: 20 }}>
      <AnimatePresence mode="popLayout" initial={false}>
        <motion.div
          key={char}
          initial={{ y: 8, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -8, opacity: 0 }}
          transition={spring}
          className={`block font-mono font-tnum text-sm font-semibold leading-5 ${isSeconds ? 'opacity-60' : ''}`}
        >
          {char}
        </motion.div>
      </AnimatePresence>
    </span>
  )
}

export default React.memo(Digit, (a, b) => a.char === b.char && !!a.isSeconds === !!b.isSeconds)

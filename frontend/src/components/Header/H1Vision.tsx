"use client"
import React from 'react'
import { motion } from 'framer-motion'
import CountUp from '../CountUp'
import Countdown from './Countdown'
import ContractLabel from './ContractLabel'
import HeroTitle from './HeroTitle'
import VisionStatement from './VisionStatement'

export default function H1Vision({ psp }: { psp?: any }) {
  const title = psp?.title ?? 'My Personal Strategic Plan'
  const contract = psp?.contract ?? null
  const vision = psp?.vision ?? psp?.visionStatement ?? ''
  const end = psp?.end_date ?? psp?.endDate
  
  return (
    <header className="mb-4 relative">
      <div className="flex items-start justify-between mt-3">
        <div>
          {contract && <ContractLabel>{contract}</ContractLabel>}
          <HeroTitle title={title} />
          {vision && <VisionStatement>{vision}</VisionStatement>}
        </div>

        <div className="ml-6">
          <div className="mt-3">
            <div className="text-[10px] uppercase tracking-widest text-[color:var(--muted-text)] mb-1">Time Remaining</div>
            <Countdown endDate={end} />
          </div>
        </div>
      </div>
    </header>
  )
}

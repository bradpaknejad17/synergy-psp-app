export function formatMetric(value: number | null | undefined, unit?: string) {
  if (value === null || value === undefined) return '—'
  if (!unit) return String(value)
  if (unit.toUpperCase() === 'USD') {
    try {
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 }).format(Number(value))
    } catch (e) {
      return String(value)
    }
  }
  // default: show integer if whole, else show up to 2 decimals
  if (Number.isInteger(value)) return `${value}`
  return Number(value).toFixed(2).replace(/\.00$/, '')
}

export function abbreviateNumber(n: number) {
  const abs = Math.abs(n)
  if (abs >= 1_000_000) return `${(n / 1_000_000).toFixed(1).replace(/\.0$/, '')}M`
  if (abs >= 1_000) return `${(n / 1_000).toFixed(1).replace(/\.0$/, '')}k`
  return String(n)
}

export function formatCompactNumber(value: number, unit?: string) {
  if (Number.isNaN(Number(value))) return String(value)
  const abs = Math.abs(value)
  let formatted: string
  if (abs >= 1_000_000) formatted = `${(value / 1_000_000).toFixed(1).replace(/\.0$/, '')}M`
  else if (abs >= 1_000) formatted = `${(value / 1_000).toFixed(1).replace(/\.0$/, '')}k`
  else formatted = String(value)

  if (unit && unit.toUpperCase() === 'USD') {
    // prepend $ for USD values
    return `$${formatted}`
  }
  return formatted
}

export function formatNumber(value: number, minFractionDigits = 0, maxFractionDigits = 2) {
  return new Intl.NumberFormat('en-US', { minimumFractionDigits: minFractionDigits, maximumFractionDigits: maxFractionDigits }).format(value)
}

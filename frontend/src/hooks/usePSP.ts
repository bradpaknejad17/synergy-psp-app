import { useEffect, useState } from 'react'
import { getPSP } from '../lib/api'

export function usePSP(pspId: string) {
  const [psp, setPsp] = useState<any | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    setLoading(true)
    getPSP(pspId)
      .then((data) => {
        if (!mounted) return
        setPsp(data)
      })
      .catch((err) => {
        console.error('Failed to fetch PSP', err)
        setError(String(err))
      })
      .finally(() => mounted && setLoading(false))

    return () => { mounted = false }
  }, [pspId])

  return { psp, loading, error }
}

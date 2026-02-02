const BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:5000'

export async function getPSP(id: string) {
  const res = await fetch(`${BASE}/api/psps/${id}`)
  if (!res.ok) throw new Error('Failed to fetch PSP')
  return res.json()
}

export async function patchTask(id: string, patch: any) {
  const res = await fetch(`${BASE}/api/tasks/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(patch)
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Failed to patch task: ${text}`)
  }
  return res.json()
}

export async function createTask(pspId: string | number, payload: any) {
  const res = await fetch(`${BASE}/api/psps/${pspId}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Failed to create task: ${text}`)
  }
  return res.json()
}

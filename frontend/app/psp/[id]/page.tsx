import React from 'react'
import PSPSingleView from '../../../src/components/PSPSingleView'

// Server component will fetch initial data in a real app.
export default function Page({ params }: { params: { id: string } }) {
  return <PSPSingleView pspId={params.id} />
}

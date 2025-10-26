import { describe, it, expect, vi } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { ServiceContainerProvider } from '../di/ServiceContainer'
import { useMatchVacancy } from '../application/useMatchVacancy'

const mockMatchService = {
  matchVacancy: vi.fn(async (vacancyId: string) => ({
    items: [
      { id: 'c1', name: 'Alice', location: 'Berlin', matchScore: 0.85 },
      { id: 'c2', name: 'Bob', location: 'Paris', matchScore: 0.7 },
    ],
    total: 2,
    vacancyId,
  })),
}

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <ServiceContainerProvider
    value={{
      matchService: mockMatchService as any,
      labelService: {} as any,
      uploadService: {} as any,
    }}
  >
    {children}
  </ServiceContainerProvider>
)

describe('useMatchVacancy', () => {
  it('fetches and sets match results', async () => {
    const { result } = renderHook(() => useMatchVacancy(), { wrapper })

    await act(async () => {
      await result.current.fetchMatches('vac-123')
    })

    expect(mockMatchService.matchVacancy).toHaveBeenCalledWith('vac-123')
    expect(result.current.state.loading).toBe(false)
    expect(result.current.state.results?.items.length).toBe(2)
  })
})
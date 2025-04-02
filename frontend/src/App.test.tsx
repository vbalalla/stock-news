import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from './App'

describe('App', () => {
  it('renders the app with navigation', () => {
    render(<App />)
    expect(screen.getByText('StockPulse Insights')).toBeInTheDocument()
  })
})

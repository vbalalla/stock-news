import { ReactNode } from 'react'
import { AppBar, Box, Container, Toolbar, Typography } from '@mui/material'
import { Link } from 'react-router-dom'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <Box className="min-h-screen bg-gray-50">
      <AppBar position="static" className="mb-4">
        <Toolbar>
          <Link to="/" className="no-underline">
            <Typography variant="h6" className="text-white">
              StockPulse Insights
            </Typography>
          </Link>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" className="py-4">
        {children}
      </Container>
    </Box>
  )
}

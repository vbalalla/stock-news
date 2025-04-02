import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { theme } from './theme'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import StockDetails from './pages/StockDetails'

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/stock/:symbol" element={<StockDetails />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  )
}

export default App

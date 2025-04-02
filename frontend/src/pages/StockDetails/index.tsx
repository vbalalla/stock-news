import { Typography } from '@mui/material'
import { useParams } from 'react-router-dom'

export default function StockDetails() {
  const { symbol } = useParams()
  
  return (
    <Typography variant="h4">
      Stock Details for {symbol}
    </Typography>
  )
}

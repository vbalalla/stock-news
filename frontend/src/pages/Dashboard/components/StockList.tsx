import { Card, CardContent, Typography, List, ListItem, ListItemButton, ListItemText, Skeleton } from '@mui/material'
import { Link } from 'react-router-dom'
import { Stock } from '../../../api/client'

interface StockListProps {
  stocks: Stock[]
  loading: boolean
}

export default function StockList({ stocks, loading }: StockListProps) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" className="mb-4">
          Top NYSE Stocks
        </Typography>
        <List className="max-h-[600px] overflow-y-auto">
          {loading ? (
            Array.from(new Array(10)).map((_, index) => (
              <ListItem key={index} disablePadding>
                <ListItemButton>
                  <Skeleton width="100%">
                    <ListItemText primary="Loading..." secondary="Loading..." />
                  </Skeleton>
                </ListItemButton>
              </ListItem>
            ))
          ) : (
            stocks.map((stock) => (
              <ListItem key={stock.symbol} disablePadding>
                <ListItemButton component={Link} to={`/stock/${stock.symbol}`}>
                  <ListItemText
                    primary={stock.symbol}
                    secondary={stock.name}
                    primaryTypographyProps={{
                      className: 'font-semibold',
                    }}
                  />
                </ListItemButton>
              </ListItem>
            ))
          )}
        </List>
      </CardContent>
    </Card>
  )
}

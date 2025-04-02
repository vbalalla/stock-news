import { useState, useEffect } from 'react'
import { Box, Typography } from '@mui/material'
import { api, Stock, NewsArticle } from '../../api/client'
import StockList from './components/StockList'
import TrendingNews from './components/TrendingNews'

export default function Dashboard() {
  const [stocks, setStocks] = useState<Stock[]>([])
  const [trendingNews, setTrendingNews] = useState<NewsArticle[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [stocksResponse, newsResponse] = await Promise.all([
          api.getStocks(),
          api.getNews()
        ])
        setStocks(stocksResponse.data)
        setTrendingNews(newsResponse.data)
      } catch (err) {
        setError('Failed to fetch data')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (error) {
    return (
      <Typography color="error" className="text-center mt-8">
        {error}
      </Typography>
    )
  }

  return (
    <Box sx={{ display: 'grid', gap: 4, gridTemplateColumns: { xs: '1fr', md: '1fr 2fr' } }}>
      <StockList stocks={stocks} loading={loading} />
      <TrendingNews news={trendingNews} loading={loading} />
    </Box>
  )
}

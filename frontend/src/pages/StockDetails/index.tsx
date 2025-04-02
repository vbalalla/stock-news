import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Box, Card, CardContent, Typography, CircularProgress } from '@mui/material'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { api, Stock, NewsArticle } from '../../api/client'
import NewsCard from '../../components/NewsCard'

export default function StockDetails() {
  const { symbol } = useParams<{ symbol: string }>()
  const [stock, setStock] = useState<Stock | null>(null)
  const [news, setNews] = useState<NewsArticle[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      if (!symbol) return
      try {
        const [stockResponse, newsResponse] = await Promise.all([
          api.getStock(symbol),
          api.getStockNews(symbol)
        ])
        setStock(stockResponse.data)
        setNews(newsResponse.data)
      } catch (err) {
        setError('Failed to fetch stock details')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [symbol])

  const sentimentData = news.reduce((acc, article) => {
    const { sentiment, sentiment_scores } = article
    acc.push({
      name: sentiment,
      positive: sentiment_scores.pos * 100,
      negative: sentiment_scores.neg * 100,
      neutral: sentiment_scores.neu * 100,
    })
    return acc
  }, [] as Array<{ name: string; positive: number; negative: number; neutral: number }>)

  if (error) {
    return (
      <Typography color="error" className="text-center mt-8">
        {error}
      </Typography>
    )
  }

  if (loading) {
    return (
      <Box className="flex justify-center items-center min-h-[400px]">
        <CircularProgress />
      </Box>
    )
  }

  if (!stock) {
    return (
      <Typography color="error" className="text-center mt-8">
        Stock not found
      </Typography>
    )
  }

  return (
    <Box>
      <Card className="mb-6">
        <CardContent>
          <Typography variant="h4" className="mb-2">
            {stock.name} ({stock.symbol})
          </Typography>
          {stock.sector && (
            <Typography variant="subtitle1" color="text.secondary">
              Sector: {stock.sector}
            </Typography>
          )}
        </CardContent>
      </Card>

      <Box sx={{ display: 'grid', gap: 4 }}>
        <Card>
          <CardContent>
            <Typography variant="h6" className="mb-4">
              Sentiment Analysis
            </Typography>
            <Box className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sentimentData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="positive" fill="#4caf50" name="Positive" />
                  <Bar dataKey="negative" fill="#f44336" name="Negative" />
                  <Bar dataKey="neutral" fill="#9e9e9e" name="Neutral" />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography variant="h6" className="mb-4">
              Latest News
            </Typography>
            <Box className="space-y-4">
              {news.map((article) => (
                <NewsCard key={article.url} article={article} />
              ))}
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Box>
  )
}

import { Card, CardContent, Typography, Grid, Skeleton } from '@mui/material'
import { NewsArticle } from '../../../api/client'
import NewsCard from '../../../components/NewsCard'

interface TrendingNewsProps {
  news: NewsArticle[]
  loading: boolean
}

export default function TrendingNews({ news, loading }: TrendingNewsProps) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" className="mb-4">
          Trending News
        </Typography>
        <Grid container spacing={2}>
          {loading ? (
            Array.from(new Array(6)).map((_, index) => (
              <Grid item xs={12} key={index}>
                <Card>
                  <CardContent>
                    <Skeleton variant="rectangular" height={200} />
                    <Skeleton width="60%" />
                    <Skeleton width="40%" />
                  </CardContent>
                </Card>
              </Grid>
            ))
          ) : (
            news.map((article) => (
              <Grid item xs={12} key={article.url}>
                <NewsCard article={article} />
              </Grid>
            ))
          )}
        </Grid>
      </CardContent>
    </Card>
  )
}

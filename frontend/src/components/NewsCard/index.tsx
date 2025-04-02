import { Card, CardContent, Typography, Chip, Link as MuiLink } from '@mui/material'
import { NewsArticle } from '../../api/client'
import { formatDistanceToNow } from 'date-fns'

interface NewsCardProps {
  article: NewsArticle
}

const getSentimentColor = (sentiment: string) => {
  switch (sentiment) {
    case 'positive':
      return 'success'
    case 'negative':
      return 'error'
    default:
      return 'default'
  }
}

export default function NewsCard({ article }: NewsCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent>
        <div className="flex justify-between items-start mb-2">
          <Typography variant="h6" className="text-lg font-semibold">
            <MuiLink
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              color="inherit"
              underline="hover"
            >
              {article.title}
            </MuiLink>
          </Typography>
          <Chip
            label={article.sentiment}
            color={getSentimentColor(article.sentiment) as any}
            size="small"
            className="ml-2"
          />
        </div>
        {article.description && (
          <Typography variant="body2" color="text.secondary" className="mb-2">
            {article.description}
          </Typography>
        )}
        <div className="flex justify-between items-center mt-2">
          <Typography variant="caption" color="text.secondary">
            {article.source} •{' '}
            {formatDistanceToNow(new Date(article.published_at), { addSuffix: true })}
          </Typography>
          {article.related_stocks.length > 0 && (
            <div className="flex gap-1">
              {article.related_stocks.map((symbol) => (
                <Chip
                  key={symbol}
                  label={symbol}
                  size="small"
                  variant="outlined"
                  className="text-xs"
                />
              ))}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

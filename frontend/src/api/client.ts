import axios from 'axios'

export interface Stock {
  symbol: string
  name: string
  market_cap: number
  sector: string
}

export interface NewsArticle {
  title: string
  description: string
  url: string
  published_at: string
  source: string
  sentiment: string
  sentiment_scores: {
    pos: number
    neg: number
    neu: number
  }
}

const apiClient = axios.create({
  baseURL: 'http://localhost:8002'
})

export const api = {
  getStocks: () => apiClient.get<Stock[]>('/stocks'),
  getStock: (symbol: string) => apiClient.get<Stock>(`/stocks/${symbol}`),
  getNews: () => apiClient.get<NewsArticle[]>('/news'),
  getStockNews: (symbol: string) => apiClient.get<NewsArticle[]>(`/news/${symbol}`)
}

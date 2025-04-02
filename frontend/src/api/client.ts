import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Stock {
  symbol: string;
  name: string;
  market_cap: number;
  sector?: string;
}

export interface NewsArticle {
  title: string;
  description?: string;
  url: string;
  published_at: string;
  source: string;
  sentiment_scores: {
    compound: number;
    pos: number;
    neg: number;
    neu: number;
  };
  sentiment: 'positive' | 'negative' | 'neutral';
  relevance_score: number;
  related_stocks: string[];
}

export const api = {
  getStocks: () => apiClient.get<Stock[]>('/stocks'),
  getStock: (symbol: string) => apiClient.get<Stock>(`/stocks/${symbol}`),
  getNews: () => apiClient.get<NewsArticle[]>('/news'),
  getStockNews: (symbol: string) => apiClient.get<NewsArticle[]>(`/news/${symbol}`),
  getTrendingNews: () => apiClient.get<NewsArticle[]>('/trending'),
};

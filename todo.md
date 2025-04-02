# StockPulse Insights - Development Todo List

**Phase 1: Backend & Basic News Aggregation**

1.  **Project Setup:**
    * [x] Set up a Python virtual environment.
    * [x] Create a Flask or FastAPI project structure.
    * [x] Initialize a Git repository.
    * [ ] Choose and set up a database (PostgreSQL or MongoDB).
    * [ ] Setup Docker and Docker-compose for local development.

2.  **Database Design:**
    * [ ] Design the `News Articles`, `Stocks`, and `Stock News Relations` database schemas.
    * [ ] Implement database models using SQLAlchemy or MongoEngine.
    * [ ] Create database migrations.

3.  **News API Integration:**
    * [x] Research and select news APIs (NewsAPI, GNews).
    * [x] Implement API client libraries (using `requests`).
    * [x] Create a service to fetch news articles based on keywords.
    * [x] Store fetched news articles in the database.
    * [ ] Implement a scheduled task (using APScheduler or Celery) to fetch news periodically.

4.  **Basic API Endpoints:**
    * [x] Create API endpoints:
        * [x] `/stocks`: Returns a list of the top 100 stocks.
        * [x] `/news`: Returns news articles.
    * [x] Implement basic error handling and logging.

**Phase 2: NLP Pipeline & Stock Data Integration**

5.  **NLP Library Setup:**
    * [ ] Install and configure spaCy or Transformers.
    * [ ] Download necessary language models.

6.  **Named Entity Recognition (NER):**
    * [x] Implement NER to identify stock symbols and company names.
    * [x] Test and refine NER accuracy.
    * [x] Link recognized entities to stock symbols in the database.

7.  **Sentiment Analysis:**
    * [x] Implement sentiment analysis using a pre-trained model.
    * [x] Store sentiment scores in the `News Articles` table.
    * [x] Test and refine sentiment analysis accuracy.

8.  **Relevance Scoring:**
    * [x] Implement a scoring algorithm based on keyword frequency and context.
    * [x] Store relevance scores in the `News Articles` table.
    * [x] Link news articles to stocks via related_stocks field.
    * [x] Test and refine relevance scoring.

9.  **Stock Data Integration:**
    * [ ] Integrate a financial API (Alpha Vantage, Polygon.io).
    * [ ] Fetch and store the list of the top 100 stocks in the database.
    * [ ] Implement a mapping between stock symbols and company names.

10. **Stock Summary Endpoint:**
    * [ ] Create the `/stock_summary` API endpoint.
    * [ ] Implement logic to summarize news and sentiment for a specific stock.

**Phase 3: Frontend & User Authentication**

11. **React Project Setup:**
    * [ ] Create a React project using Create React App or Vite.
    * [ ] Set up TypeScript.
    * [ ] Choose and install UI and charting libraries.
    * [ ] Setup Axios or fetch for API calls.

12. **Dashboard Component:**
    * [ ] Create the dashboard component.
    * [ ] Display trending news.
    * [ ] Implement a search bar for stocks.
    * [ ] Display a stock watchlist (initially static).

13. **Stock Details Page:**
    * [ ] Create the stock details page.
    * [ ] Display stock-specific news feed.
    * [ ] Visualize sentiment analysis using charts.
    * [ ] Display news summaries.

14. **User Authentication:**
    * [ ] Implement user registration and login functionality in the backend.
    * [ ] Create corresponding frontend components.
    * [ ] Implement JWT authentication.
    * [ ] Secure API endpoints.

15. **User Watchlist:**
    * [ ] Implement watchlist functionality in the backend and frontend.
    * [ ] Allow users to add and remove stocks from their watchlist.

**Phase 4: Optimization, Deployment, and Maintenance**

16. **Performance Optimization:**
    * [ ] Optimize database queries.
    * [ ] Implement caching.
    * [ ] Optimize frontend performance.

17. **Deployment Setup:**
    * [ ] Create Dockerfiles for backend and frontend.
    * [ ] Configure a CI/CD pipeline (e.g., using GitHub Actions).
    * [ ] Deploy to a cloud platform (AWS, Google Cloud, Azure).

18. **Monitoring and Logging:**
    * [ ] Implement logging and monitoring.
    * [ ] Set up alerts.

19. **Continuous Improvement:**
    * [ ] Add more news sources.
    * [ ] Implement user feedback features.
    * [ ] Refine NLP models.
    * [ ] Address bugs and improve performance.
    * [ ] Add more features.
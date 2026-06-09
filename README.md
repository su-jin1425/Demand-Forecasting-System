# Demand Forecasting System

A scalable, enterprise-grade demand forecasting platform built to predict business trends using statistical modeling and machine learning. This system is designed to handle time-series forecasting, automated model retraining, and real-time inference while maintaining high performance and reliability.

## 🏗️ System Architecture

The application relies on a modular, microservices-inspired architecture managed through Docker Compose, ensuring clean separation of concerns and robust scalability.

### Core Subsystems

1. **API Gateway (FastAPI)**
   - Acts as the primary entry point for all client requests.
   - Handles JWT-based authentication, request validation, and routing.
   - Fully asynchronous, ensuring that the event loop is never blocked by I/O operations.

2. **Machine Learning Engine & Workers (Celery + Redis)**
   - **Queue Broker:** Redis acts as the message broker for background task distribution.
   - **Background Processing:** Celery workers handle all CPU-intensive machine learning tasks (training, evaluation, and prediction).
   - This decoupling is critical: it guarantees that heavy model training processes never degrade the response time of the customer-facing API.

3. **Database Layer (PostgreSQL)**
   - Stores user data, model metadata, historical predictions, and analytics metrics.
   - Interacted with purely via asynchronous operations (`asyncpg`) and SQLAlchemy models, with schema versioning tracked by Alembic.

4. **Observability Stack (Prometheus + Grafana)**
   - FastAPI `/metrics` are scraped continuously.
   - Allows for real-time monitoring of API latency, background task queue lengths, and model accuracy drift.

## 🧠 Machine Learning & Feature Engineering

### Forecasting Strategy Pattern
The system implements a unified `BasePredictor` interface that dynamically wraps multiple algorithms depending on the requested configuration:
- **Prophet:** For capturing complex weekly/yearly seasonality and holiday effects.
- **XGBoost:** A gradient boosting approach optimized for non-linear feature interactions.
- **SARIMAX (Statsmodels):** Traditional statistical modeling for autoregressive trends.

### Automated Feature Engineering
To maximize model accuracy (specifically for XGBoost), the system includes a dedicated `FeatureEngineer` pipeline that dynamically transforms raw time-series data into rich feature matrices. It automatically extracts:
- Temporal identifiers (month, day of week, weekend flags).
- Autoregressive lag features (`t-1`, `t-7`, `t-14`).
- Rolling window statistics (7-day moving averages and standard deviations).

## 🚀 Deployment & Installation

The entire infrastructure is containerized and can be launched with a single command.

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (if running outside of Docker)

### Local Deployment

1. **Clone and Setup Environment**
   ```bash
   cp .env.example .env
   ```
2. **Start the Infrastructure**
   ```bash
   docker-compose up --build -d
   ```
3. **Run Database Migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

### Accessing the Services
- **FastAPI Backend:** `http://localhost:8000`
- **Swagger API Docs:** `http://localhost:8000/docs`
- **Prometheus:** `http://localhost:9090`
- **Grafana:** `http://localhost:3000`

## 📡 Core API Endpoints

- `POST /api/v1/auth/register` & `login`: JWT Authentication layer.
- `POST /api/v1/models/train`: Asynchronously triggers a Celery worker to train a requested model (Prophet, XGBoost, or Statsmodels).
- `GET /api/v1/analytics/accuracy-improvement`: Benchmarks and validates organic error reduction via the implemented feature engineering pipelines against naive baselines.
# Data Lakehouse Architecture Simulation

A complete local data lakehouse implementation with three data layers: raw, clean, and analytics. Ingests weather data from OpenWeather API and CSV files, then transforms them through a production-grade pipeline with Apache Airflow orchestration.

## 🚀 Quick Start

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

### Run Once (Manual)

```bash
python3 scripts/run_pipeline.py
```

### Run with Apache Airflow (Recommended)

```bash
# Setup Airflow
bash scripts/setup_airflow.sh

# Terminal 1: Start webserver
airflow webserver -p 8080

# Terminal 2: Start scheduler
airflow scheduler

# Access: http://localhost:8080 (admin/admin)
```

## 📊 Architecture

**Three-Layer Lakehouse:**
- **Raw (Bronze)** - Original untransformed data (JSON, CSV)
- **Clean (Silver)** - Normalized, deduplicated data
- **Analytics (Gold)** - Optimized DuckDB tables and SQL views

**Data Flow:**
```
API Data + CSV Files → Raw Layer → Clean Layer → DuckDB Database → Analytics Report
```

## 📁 Project Structure

```
data-lakehouse-simulation/
├── config/config.py                    # Configuration management
├── dags/                               # Airflow DAGs (scheduled pipelines)
│   ├── main_pipeline_dag.py           # Daily ETL orchestration (2:00 AM UTC)
│   └── data_generation_dag.py         # Weekly sample data generation

├── src/
│   ├── ingestion/
│   │   ├── api_ingestion.py           # OpenWeather API ingestion
│   │   └── csv_ingestion.py           # CSV file ingestion
│   ├── transformations/
│   │   ├── raw_to_clean.py            # Flatten & normalize
│   │   └── clean_to_analytics.py      # Create DuckDB tables
│   └── analytics/
│       └── queries.py                  # SQL queries & reports
├── scripts/
│   ├── run_pipeline.py                # Main orchestration
│   ├── generate_sample_data.py        # Generate test CSV
│   └── setup_airflow.sh               # Airflow initialization
├── data/
│   ├── raw/                           # Original data
│   ├── clean/                         # Normalized data
│   └── analytics/                     # DuckDB database + reports
├── airflow_home/                      # Airflow working directory (created on setup)
├── .env                               # API key (git ignored)
├── airflow.cfg                        # Airflow configuration
└── requirements.txt                   # Python dependencies
```

## 🔧 Technologies

- **Python 3.8+** - Core processing language
- **Apache Airflow** - Workflow orchestration & scheduling
- **OpenWeather API** - Weather data source
- **Pandas** - Data processing
- **DuckDB** - Analytical database (local, serverless)

## ⏰ Scheduling with Airflow

### Available DAGs:

| DAG | Schedule | Purpose |
|-----|----------|---------|
| `data_lakehouse_pipeline` | Daily @ 2:00 AM UTC | Complete ETL pipeline |
| `data_generation_pipeline` | Weekly (Sunday midnight) | Generate test data |

### Monitor Execution:

- **Webserver UI**: http://localhost:8080
- **Logs**: `airflow_home/logs/`
- **Database**: `airflow_home/airflow.db`

## 📈 Output

After running the pipeline:

- **Raw Data** - `data/raw/api/*.json` and `data/raw/csv/*.csv`
- **Clean Data** - `data/clean/*.csv`
- **Database** - `data/analytics/lakehouse.duckdb`
- **Report** - `data/analytics/analytics_report.json`
- **Analytics Views** - `data/analytics/*.csv` (exported)

The analytics report includes:
- Overall weather statistics (5 cities, 150 records)
- Latest temperatures by city
- Weather condition distribution
- Extreme weather events

## 🎯 Features

✅ Apache Airflow orchestration with task groups
✅ Real-time API data ingestion with error handling
✅ CSV file processing with metadata tracking
✅ Data validation and quality checks
✅ Automatic table creation in DuckDB
✅ Multiple analytical views (daily summary, city comparison)
✅ Comprehensive JSON report generation
✅ Fully typed Python code with docstrings
✅ Production-ready error handling and logging
✅ Scheduled automation (no manual intervention needed)

## 💡 Usage Examples

### Manual Execution:

```bash
python3 scripts/run_pipeline.py
```

### Airflow Execution:

```bash
# Trigger specific DAG
airflow dags trigger data_lakehouse_pipeline

# Check DAG status
airflow dags list
airflow tasks list data_lakehouse_pipeline
```

### Query Analytics:

```python
from src.analytics.queries import AnalyticsQueryEngine

engine = AnalyticsQueryEngine()
summary = engine.get_weather_summary()
print(summary)
```

## 🔐 Security

- API keys stored in `.env` file (git-ignored)
- Airflow secret key in `airflow.cfg` (change in production)
- No credentials in source code
- Environment-based configuration

## 📝 License

Open source project for educational and portfolio purposes.

cities = engine.get_city_temperatures()

# Generate full report
report = engine.generate_analytics_report()
```

## 🔐 Security

API keys are stored in `.env` and git-ignored. Never commit credentials to version control.

## 📝 License

Open source project for educational and portfolio purposes.

# Data Lakehouse Architecture Simulation

A complete local data lakehouse implementation with three data layers: raw, clean, and analytics. Ingests weather data from OpenWeather API and CSV files, then transforms them through a production-grade pipeline.

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

Or edit `.env` directly with your OpenWeather API key.

### Run the Pipeline

```bash
python3 scripts/run_pipeline.py
```

This will:
1. **Ingest** - Fetch weather data from OpenWeather API + CSV files
2. **Transform** - Normalize and flatten data
3. **Analyze** - Create DuckDB tables and run analytics

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
│   └── generate_sample_data.py        # Generate test CSV
├── data/
│   ├── raw/                           # Original data
│   ├── clean/                         # Normalized data
│   └── analytics/                     # DuckDB database + reports
├── .env                               # API key (git ignored)
└── requirements.txt                   # Python dependencies
```

## 🔧 Technologies

- **Python 3.8+** - Core processing language
- **OpenWeather API** - Weather data source
- **Pandas** - Data processing
- **DuckDB** - Analytical database (local, serverless)
- **Python-dotenv** - Environment variable management

## 📈 Output

After running the pipeline:

- **Raw Data** - `data/raw/api/*.json` and `data/raw/csv/*.csv`
- **Clean Data** - `data/clean/*.csv`
- **Database** - `data/analytics/lakehouse.duckdb`
- **Report** - `data/analytics/analytics_report.json`

The analytics report includes:
- Overall weather statistics
- Latest temperatures by city
- Temperature trends over time
- Weather condition distribution
- Extreme weather events

## 🎯 Features

✅ Real-time API data ingestion with error handling
✅ CSV file processing with metadata tracking
✅ Data validation and quality checks
✅ Automatic table creation in DuckDB
✅ Multiple analytical views (daily summary, city comparison)
✅ Comprehensive JSON report generation
✅ Fully typed Python code with docstrings
✅ Production-ready error handling and logging

## 💡 Usage Examples

```python
from src.analytics.queries import AnalyticsQueryEngine

# Initialize the analytics engine
engine = AnalyticsQueryEngine()

# Get weather summary
summary = engine.get_weather_summary()

# Get temperatures by city
cities = engine.get_city_temperatures()

# Generate full report
report = engine.generate_analytics_report()
```

## 🔐 Security

API keys are stored in `.env` and git-ignored. Never commit credentials to version control.

## 📝 License

Open source project for educational and portfolio purposes.

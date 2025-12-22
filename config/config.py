"""
Configuration module for the data lakehouse simulation.
Manages paths, API endpoints, and system settings.
"""

import os
from pathlib import Path
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data layer paths (simulate cloud storage like S3)
DATA_ROOT = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_ROOT / "raw"
RAW_API_PATH = RAW_DATA_PATH / "api"
RAW_CSV_PATH = RAW_DATA_PATH / "csv"
CLEAN_DATA_PATH = DATA_ROOT / "clean"
ANALYTICS_DATA_PATH = DATA_ROOT / "analytics"

# Database paths
DUCKDB_PATH = ANALYTICS_DATA_PATH / "lakehouse.duckdb"

# API Configuration
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Load from .env file
WEATHER_CITIES = [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"name": "London", "lat": 51.5074, "lon": -0.1278},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
]

# Ingestion settings
INGESTION_BATCH_SIZE = 100
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMEZONE = pytz.timezone("UTC")

# CSV file paths (sample data)
SAMPLE_CSV_FILE = RAW_CSV_PATH / "historical_data.csv"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Ensure directories exist
def create_directories():
    """Create all necessary directories if they don't exist."""
    for path in [RAW_API_PATH, RAW_CSV_PATH, CLEAN_DATA_PATH, ANALYTICS_DATA_PATH]:
        path.mkdir(parents=True, exist_ok=True)

create_directories()

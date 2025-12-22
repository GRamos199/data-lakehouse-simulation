"""
API Ingestion Module - Fetches weather data from OpenWeather API and stores as JSON.
Maps to cloud architecture: AWS Lambda + S3 (raw/api/)
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import requests
from config.config import (
    OPENWEATHER_API_URL,
    OPENWEATHER_API_KEY,
    WEATHER_CITIES,
    RAW_API_PATH,
    TIMESTAMP_FORMAT,
    TIMEZONE,
)

logger = logging.getLogger(__name__)

class APIIngestionManager:
    """Manages ingestion of data from external APIs."""

    def __init__(self, api_key: str = OPENWEATHER_API_KEY):
        self.api_key = api_key
        self.api_url = OPENWEATHER_API_URL
        self.raw_path = RAW_API_PATH

    def fetch_weather_data(self, city_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch weather data from OpenWeather API.
        
        Args:
            city_config: Dictionary with 'name', 'lat', 'lon' keys
            
        Returns:
            API response as dictionary or None if request fails
        """
        try:
            params = {
                "lat": city_config["lat"],
                "lon": city_config["lon"],
                "appid": self.api_key,
                "units": "metric",
            }
            
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            # Add ingestion metadata
            data["_ingestion_timestamp"] = datetime.now(TIMEZONE).isoformat()
            data["_source"] = "openweather_api"
            data["_city_name"] = city_config["name"]
            
            logger.info(f"Successfully fetched data for {city_config['name']}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {city_config['name']}: {str(e)}")
            return None

    def ingest_all_cities(self) -> List[str]:
        """
        Ingest weather data for all configured cities.
        
        Returns:
            List of file paths where data was stored
        """
        ingested_files = []
        
        for city_config in WEATHER_CITIES:
            data = self.fetch_weather_data(city_config)
            
            if data:
                file_path = self._save_raw_data(data, city_config["name"])
                if file_path:
                    ingested_files.append(str(file_path))
        
        logger.info(f"Ingestion complete. Stored {len(ingested_files)} files.")
        return ingested_files

    def _save_raw_data(self, data: Dict[str, Any], city_name: str) -> Path:
        """
        Save API response as JSON file in raw layer.
        File naming convention: city_YYYY-MM-DD_HH-MM-SS.json
        
        Args:
            data: API response data
            city_name: City name for file naming
            
        Returns:
            Path to saved file
        """
        try:
            timestamp = datetime.now(TIMEZONE).strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{city_name.lower().replace(' ', '_')}_{timestamp}.json"
            file_path = self.raw_path / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved raw data to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving data for {city_name}: {str(e)}")
            return None

    def ingest_incremental(self, last_timestamp: str = None) -> List[str]:
        """
        Incremental ingestion - only fetch data newer than last_timestamp.
        This supports incremental loads in production scenarios.
        
        Args:
            last_timestamp: ISO format timestamp of last ingestion
            
        Returns:
            List of newly ingested file paths
        """
        logger.info(f"Starting incremental ingestion from {last_timestamp}")
        # In a real system, this would check if data has changed since last_timestamp
        # For simulation, we'll just fetch all data
        return self.ingest_all_cities()


# Utility function for direct use
def ingest_weather_data(api_key: str = OPENWEATHER_API_KEY) -> List[str]:
    """Simple function to trigger weather data ingestion."""
    manager = APIIngestionManager(api_key)
    return manager.ingest_all_cities()

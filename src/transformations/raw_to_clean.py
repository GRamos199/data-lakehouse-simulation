"""
Raw to Clean Transformation Module - Normalizes and flattens JSON and CSV data.
Maps to cloud architecture: AWS Glue + S3 (clean/)
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from config.config import (
    CLEAN_DATA_PATH,
    RAW_API_PATH,
    RAW_CSV_PATH,
    TIMEZONE,
)

logger = logging.getLogger(__name__)


class RawToCleanTransformer:
    """Transforms data from raw layer to clean (normalized) layer."""

    def __init__(self):
        self.raw_api_path = RAW_API_PATH
        self.raw_csv_path = RAW_CSV_PATH
        self.clean_path = CLEAN_DATA_PATH

    def transform_weather_data(self) -> List[str]:
        """
        Transform raw JSON weather data into normalized CSV format.
        Flattens nested structures and removes unnecessary fields.

        Returns:
            List of cleaned file paths
        """
        cleaned_files = []

        for raw_file in self.raw_api_path.glob("*.json"):
            try:
                with open(raw_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Flatten the weather data structure
                cleaned_record = self._flatten_weather_json(data)

                # Save as CSV
                df = pd.DataFrame([cleaned_record])
                clean_filename = f"{raw_file.stem}_clean.csv"
                clean_path = self.clean_path / clean_filename

                df.to_csv(clean_path, index=False)
                cleaned_files.append(str(clean_path))

                logger.info(
                    f"Transformed weather data: {raw_file.name} -> {clean_filename}"
                )

            except Exception as e:
                logger.error(f"Error transforming {raw_file.name}: {str(e)}")

        return cleaned_files

    def transform_csv_data(self) -> List[str]:
        """
        Transform raw CSV data (legacy format) to clean layer.
        Applies data quality checks and standardization.

        Returns:
            List of cleaned file paths
        """
        cleaned_files = []

        for raw_file in self.raw_csv_path.glob("*.csv"):
            try:
                # Read raw CSV
                df = pd.read_csv(raw_file)

                # Apply transformations
                df = self._standardize_csv(df)

                # Save cleaned version
                clean_filename = f"{raw_file.stem}_clean.csv"
                clean_path = self.clean_path / clean_filename

                df.to_csv(clean_path, index=False)
                cleaned_files.append(str(clean_path))

                logger.info(
                    f"Transformed CSV data: {raw_file.name} -> {clean_filename}"
                )
                logger.info(f"Rows: {len(df)}, Columns: {len(df.columns)}")

            except Exception as e:
                logger.error(f"Error transforming {raw_file.name}: {str(e)}")

        return cleaned_files

    @staticmethod
    def _flatten_weather_json(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flatten nested JSON weather structure.

        Input example:
            {
                "coord": {"lon": -74.0060, "lat": 40.7128},
                "main": {"temp": 15.2, "humidity": 65},
                ...
            }

        Output: Flattened key-value pairs
        """
        flattened = {}

        # Main fields
        flattened["city_name"] = data.get("name", "")
        flattened["country"] = data.get("sys", {}).get("country", "")
        flattened["latitude"] = data.get("coord", {}).get("lat", "")
        flattened["longitude"] = data.get("coord", {}).get("lon", "")

        # Weather condition
        weather = data.get("weather", [{}])[0]
        flattened["weather_main"] = weather.get("main", "")
        flattened["weather_description"] = weather.get("description", "")

        # Temperature and pressure
        main = data.get("main", {})
        flattened["temperature"] = main.get("temp", "")
        flattened["feels_like"] = main.get("feels_like", "")
        flattened["temp_min"] = main.get("temp_min", "")
        flattened["temp_max"] = main.get("temp_max", "")
        flattened["pressure"] = main.get("pressure", "")
        flattened["humidity"] = main.get("humidity", "")

        # Wind and visibility
        flattened["wind_speed"] = data.get("wind", {}).get("speed", "")
        flattened["wind_direction"] = data.get("wind", {}).get("deg", "")
        flattened["visibility"] = data.get("visibility", "")

        # Clouds
        flattened["cloudiness"] = data.get("clouds", {}).get("all", "")

        # Metadata
        flattened["ingestion_timestamp"] = data.get("_ingestion_timestamp", "")
        flattened["data_source"] = data.get("_source", "")
        flattened["fetch_timestamp"] = datetime.fromtimestamp(
            data.get("dt", 0), tz=TIMEZONE
        ).isoformat()

        return flattened

    @staticmethod
    def _standardize_csv(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize CSV data: clean column names, handle missing values.
        """
        # Standardize column names: lowercase, replace spaces with underscores
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Handle missing values - fill with appropriate defaults based on column type
        for col in df.columns:
            if df[col].dtype in ["float64", "int64"]:
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna("N/A")

        return df

    def run_all_transformations(self) -> Dict[str, List[str]]:
        """Run all transformation processes."""
        logger.info("Starting raw to clean transformations...")

        results = {
            "weather_files": self.transform_weather_data(),
            "csv_files": self.transform_csv_data(),
        }

        logger.info(
            f"Transformation complete. Weather files: {len(results['weather_files'])}, "
            f"CSV files: {len(results['csv_files'])}"
        )

        return results


def transform_raw_to_clean() -> Dict[str, List[str]]:
    """Simple function to trigger raw to clean transformation."""
    transformer = RawToCleanTransformer()
    return transformer.run_all_transformations()

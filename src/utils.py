"""
Utility functions for data validation, error handling, and common operations.
"""

import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates data against expected schemas."""

    @staticmethod
    def validate_weather_data(data: Dict[str, Any]) -> bool:
        """
        Validate weather data structure from OpenWeather API.

        Args:
            data: Weather data dictionary

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["coord", "main", "weather", "dt", "sys", "id", "name"]
        required_main_fields = ["temp", "feels_like", "humidity", "pressure"]

        # Check top-level fields
        if not all(field in data for field in required_fields):
            logger.warning(
                f"Missing required fields in weather data: {data.get('name', 'unknown')}"
            )
            return False

        # Check main/temperature fields
        if not all(field in data.get("main", {}) for field in required_main_fields):
            logger.warning(
                f"Missing required main fields in weather data: {data.get('name', 'unknown')}"
            )
            return False

        # Check weather array
        if not isinstance(data.get("weather"), list) or len(data["weather"]) == 0:
            logger.warning(
                f"Weather array missing or empty: {data.get('name', 'unknown')}"
            )
            return False

        return True

    @staticmethod
    def validate_dataframe_schema(df, required_columns: List[str]) -> bool:
        """
        Validate that a DataFrame has all required columns.

        Args:
            df: pandas DataFrame
            required_columns: List of column names that must exist

        Returns:
            True if all columns exist, False otherwise
        """
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            logger.warning(f"DataFrame missing columns: {missing_cols}")
            return False
        return True


class FileHashManager:
    """Manages file hashing for data integrity verification."""

    @staticmethod
    def calculate_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
        """
        Calculate hash of a file for integrity verification.

        Args:
            file_path: Path to file
            algorithm: Hash algorithm to use (default: sha256)

        Returns:
            Hex string of file hash
        """
        hash_func = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    @staticmethod
    def save_file_manifest(directory: Path, manifest_file: Path) -> None:
        """
        Create a manifest of all files in a directory with their hashes.

        Args:
            directory: Directory to scan
            manifest_file: Path to save manifest
        """
        manifest = {}
        for file_path in directory.glob("**/*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(directory)
                manifest[str(relative_path)] = FileHashManager.calculate_file_hash(
                    file_path
                )

        with open(manifest_file, "w") as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"Manifest saved with {len(manifest)} files to {manifest_file}")


class MetricsCollector:
    """Collects pipeline execution metrics."""

    def __init__(self):
        self.metrics = {"start_time": datetime.now().isoformat(), "stages": {}}

    def record_stage(
        self,
        stage_name: str,
        status: str,
        duration_seconds: float,
        record_count: int = 0,
        additional_info: Optional[Dict] = None,
    ) -> None:
        """
        Record metrics for a pipeline stage.

        Args:
            stage_name: Name of the pipeline stage
            status: 'success', 'failure', or 'warning'
            duration_seconds: How long the stage took
            record_count: Number of records processed
            additional_info: Additional metric data
        """
        self.metrics["stages"][stage_name] = {
            "status": status,
            "duration_seconds": duration_seconds,
            "record_count": record_count,
            "timestamp": datetime.now().isoformat(),
            "additional_info": additional_info or {},
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        self.metrics["end_time"] = datetime.now().isoformat()
        return self.metrics

    def save_metrics(self, output_path: Path) -> None:
        """Save metrics to JSON file."""
        with open(output_path, "w") as f:
            json.dump(self.get_metrics(), f, indent=2, default=str)
        logger.info(f"Metrics saved to {output_path}")


class ErrorHandler:
    """Centralized error handling and reporting."""

    @staticmethod
    def handle_api_error(error: Exception, context: str) -> None:
        """Handle and log API errors."""
        logger.error(f"API Error in {context}: {str(error)}", exc_info=True)

    @staticmethod
    def handle_data_error(
        error: Exception, context: str, data_sample: Any = None
    ) -> None:
        """Handle and log data processing errors."""
        logger.error(f"Data Error in {context}: {str(error)}", exc_info=True)
        if data_sample:
            logger.debug(f"Data sample: {data_sample}")

    @staticmethod
    def handle_io_error(error: Exception, file_path: Path) -> None:
        """Handle and log file I/O errors."""
        logger.error(f"IO Error accessing {file_path}: {str(error)}", exc_info=True)

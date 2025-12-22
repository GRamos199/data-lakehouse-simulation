"""
CSV Ingestion Module - Ingests CSV files as-is into raw layer.
Maps to cloud architecture: AWS S3 (raw/csv/)
"""

import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from config.config import (
    RAW_CSV_PATH,
    TIMESTAMP_FORMAT,
    TIMEZONE,
)

logger = logging.getLogger(__name__)

class CSVIngestionManager:
    """Manages ingestion of CSV files into the raw layer."""

    def __init__(self):
        self.raw_path = RAW_CSV_PATH

    def ingest_csv_file(self, source_file_path: str) -> Tuple[bool, str]:
        """
        Ingest a CSV file by copying it to the raw layer.
        Adds ingestion metadata in a companion JSON file.
        
        Args:
            source_file_path: Path to source CSV file
            
        Returns:
            Tuple of (success: bool, destination_path: str)
        """
        try:
            source_path = Path(source_file_path)
            
            if not source_path.exists():
                logger.error(f"Source file not found: {source_file_path}")
                return False, ""
            
            # Create destination filename with timestamp
            timestamp = datetime.now(TIMEZONE).strftime("%Y-%m-%d_%H-%M-%S")
            dest_filename = f"{source_path.stem}_{timestamp}.csv"
            dest_path = self.raw_path / dest_filename
            
            # Copy file
            with open(source_path, 'r', encoding='utf-8') as src:
                with open(dest_path, 'w', encoding='utf-8', newline='') as dst:
                    dst.write(src.read())
            
            # Count rows for metadata
            row_count = sum(1 for _ in open(dest_path)) - 1  # Exclude header
            
            # Create metadata file
            metadata = {
                "_ingestion_timestamp": datetime.now(TIMEZONE).isoformat(),
                "_source": "csv_file",
                "_source_filename": source_path.name,
                "_destination_filename": dest_filename,
                "_row_count": row_count,
            }
            
            metadata_path = dest_path.with_suffix('.json')
            import json
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Successfully ingested CSV: {source_file_path} -> {dest_path}")
            logger.info(f"Row count: {row_count}")
            
            return True, str(dest_path)
            
        except Exception as e:
            logger.error(f"Error ingesting CSV file {source_file_path}: {str(e)}")
            return False, ""

    def list_raw_csv_files(self) -> List[Path]:
        """List all CSV files in the raw CSV layer."""
        return list(self.raw_path.glob("*.csv"))

    def get_csv_stats(self) -> dict:
        """Get statistics about ingested CSV files."""
        csv_files = self.list_raw_csv_files()
        total_files = len(csv_files)
        total_size_mb = sum(f.stat().st_size for f in csv_files) / (1024 * 1024)
        
        return {
            "total_files": total_files,
            "total_size_mb": round(total_size_mb, 2),
            "files": [str(f.name) for f in csv_files],
        }


def ingest_csv(source_file_path: str) -> Tuple[bool, str]:
    """Simple function to trigger CSV ingestion."""
    manager = CSVIngestionManager()
    return manager.ingest_csv_file(source_file_path)

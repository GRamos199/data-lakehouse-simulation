"""
Clean to Analytics Transformation Module - Creates analytical tables and models.
Maps to cloud architecture: Snowflake / Data Warehouse
"""

import logging
import pandas as pd
from pathlib import Path
from typing import List, Dict
import duckdb
from config.config import (
    CLEAN_DATA_PATH,
    DUCKDB_PATH,
    ANALYTICS_DATA_PATH,
)

logger = logging.getLogger(__name__)

class CleanToAnalyticsTransformer:
    """Transforms cleaned data into analytical tables using DuckDB."""

    def __init__(self):
        self.clean_path = CLEAN_DATA_PATH
        self.analytics_path = ANALYTICS_DATA_PATH
        self.duckdb_path = DUCKDB_PATH
        self.conn = None

    def connect(self):
        """Connect to DuckDB database."""
        try:
            self.conn = duckdb.connect(str(self.duckdb_path))
            logger.info(f"Connected to DuckDB at {self.duckdb_path}")
        except Exception as e:
            logger.error(f"Failed to connect to DuckDB: {str(e)}")
            raise

    def disconnect(self):
        """Close DuckDB connection."""
        if self.conn:
            self.conn.close()

    def create_weather_analytics_table(self) -> bool:
        """Create analytics table for weather data."""
        try:
            # Find weather CSV files in clean layer
            weather_files = list(self.clean_path.glob("*_clean.csv"))
            
            if not weather_files:
                logger.info("No weather CSV files found in clean layer")
                return False
            
            # Load and combine all clean weather data
            dfs = []
            for weather_file in weather_files:
                try:
                    df = pd.read_csv(weather_file)
                    dfs.append(df)
                    logger.info(f"Loaded data from {weather_file.name}")
                except Exception as e:
                    logger.warning(f"Could not load {weather_file.name}: {str(e)}")
            
            if not dfs:
                logger.warning("No valid CSV files to load")
                return False
            
            # Combine all dataframes
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Drop existing table if present
            self.conn.execute("DROP TABLE IF EXISTS weather_analytics")
            
            # Register dataframe and create persistent table
            self.conn.register("_temp_weather", combined_df)
            self.conn.execute("CREATE TABLE weather_analytics AS SELECT * FROM _temp_weather")
            
            logger.info("Weather analytics table created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating weather analytics table: {str(e)}")
            return False

    def create_aggregated_analytics_views(self) -> bool:
        """Create aggregated views for analytical queries."""
        try:
            # Daily summary view
            self.conn.execute("""
            CREATE OR REPLACE VIEW daily_weather_summary AS
            SELECT
                city,
                date,
                ROUND(AVG(temperature_high), 2) as avg_temp_high,
                ROUND(AVG(temperature_low), 2) as avg_temp_low,
                ROUND(AVG(humidity), 1) as avg_humidity,
                ROUND(AVG(wind_speed_kmh), 2) as avg_wind_speed,
                COUNT(*) as record_count
            FROM weather_analytics
            GROUP BY city, date
            ORDER BY city, date DESC
            """)
            
            # City comparison view
            self.conn.execute("""
            CREATE OR REPLACE VIEW city_comparison AS
            SELECT
                city,
                condition,
                ROUND(AVG(temperature_high), 2) as avg_temp_high,
                ROUND(AVG(temperature_low), 2) as avg_temp_low,
                MAX(humidity) as max_humidity,
                COUNT(*) as observations
            FROM weather_analytics
            GROUP BY city, condition
            ORDER BY city, avg_temp_high DESC
            """)
            
            logger.info("Analytical views created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating analytical views: {str(e)}")
            return False

    def export_analytics_tables(self) -> List[str]:
        """Export analytical tables to Parquet format for archival."""
        exported_files = []
        
        try:
            # Export weather analytics table
            if self._table_exists("weather_analytics"):
                output_file = self.analytics_path / "weather_analytics.parquet"
                self.conn.execute(f"COPY weather_analytics TO '{output_file}' (FORMAT PARQUET)")
                exported_files.append(str(output_file))
                logger.info(f"Exported weather_analytics to {output_file}")
            
            # Export views to CSV
            views = ["daily_weather_summary", "city_comparison"]
            for view in views:
                if self._table_exists(view):
                    output_file = self.analytics_path / f"{view}.csv"
                    self.conn.execute(f"COPY (SELECT * FROM {view}) TO '{output_file}' (FORMAT CSV, HEADER TRUE)")
                    exported_files.append(str(output_file))
                    logger.info(f"Exported {view} to {output_file}")
            
        except Exception as e:
            logger.error(f"Error exporting analytics tables: {str(e)}")
        
        return exported_files

    def _table_exists(self, table_name: str) -> bool:
        """Check if a table or view exists."""
        try:
            result = self.conn.execute(
                f"SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}'"
            ).fetchall()
            return len(result) > 0
        except:
            return False

    def get_analytics_summary(self) -> Dict:
        """Get summary statistics of analytics layer."""
        summary = {}
        
        try:
            if self._table_exists("weather_analytics"):
                row_count = self.conn.execute(
                    "SELECT COUNT(*) FROM weather_analytics"
                ).fetchone()[0]
                summary["weather_analytics_rows"] = row_count
                
                cities = self.conn.execute(
                    "SELECT DISTINCT city_name FROM weather_analytics"
                ).fetchall()
                summary["cities_loaded"] = [city[0] for city in cities]
                
        except Exception as e:
            logger.error(f"Error generating analytics summary: {str(e)}")
        
        return summary

    def run_all_transformations(self) -> Dict:
        """Run complete clean to analytics transformation pipeline."""
        logger.info("Starting clean to analytics transformations...")
        
        try:
            self.connect()
            
            # Create main analytics tables
            self.create_weather_analytics_table()
            
            # Create analytical views
            self.create_aggregated_analytics_views()
            
            # Export analytics artifacts
            exported = self.export_analytics_tables()
            
            # Get summary
            summary = self.get_analytics_summary()
            
            logger.info("Clean to analytics transformation complete")
            
            return {
                "status": "success",
                "exported_files": exported,
                "summary": summary,
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            return {"status": "failed", "error": str(e)}
        finally:
            self.disconnect()


def transform_clean_to_analytics() -> Dict:
    """Simple function to trigger clean to analytics transformation."""
    transformer = CleanToAnalyticsTransformer()
    return transformer.run_all_transformations()

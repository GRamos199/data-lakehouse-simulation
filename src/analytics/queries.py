"""
Analytics Query Module - Provides analytical insights using SQL.
Maps to cloud architecture: Snowflake / Tableau / BI Tools
"""

import logging
from typing import List, Dict, Any
import duckdb
from config.config import DUCKDB_PATH

logger = logging.getLogger(__name__)

class AnalyticsQueryEngine:
    """Executes analytical queries against the data warehouse."""

    def __init__(self):
        self.duckdb_path = DUCKDB_PATH
        self.conn = None

    def connect(self):
        """Connect to DuckDB database."""
        try:
            self.conn = duckdb.connect(str(self.duckdb_path))
        except Exception as e:
            logger.error(f"Failed to connect to DuckDB: {str(e)}")
            raise

    def disconnect(self):
        """Close DuckDB connection."""
        if self.conn:
            self.conn.close()

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results as list of dictionaries."""
        try:
            result = self.conn.execute(query).fetchall()
            columns = [desc[0] for desc in self.conn.description]
            return [dict(zip(columns, row)) for row in result]
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            return []

    def get_weather_summary(self) -> Dict[str, Any]:
        """Get high-level weather summary across all cities."""
        query = """
        SELECT
            COUNT(DISTINCT city) as total_cities,
            COUNT(*) as total_records,
            ROUND(AVG(temperature_high), 2) as avg_temp_high,
            ROUND(AVG(temperature_low), 2) as avg_temp_low,
            MAX(temperature_high) as hottest,
            MIN(temperature_low) as coldest,
            ROUND(AVG(humidity), 1) as avg_humidity
        FROM weather_analytics
        """
        results = self.execute_query(query)
        return results[0] if results else {}

    def get_city_temperatures(self) -> List[Dict[str, Any]]:
        """Get latest weather for each city."""
        query = """
        SELECT * FROM weather_analytics
        ORDER BY city, date DESC
        LIMIT 10
        """
        return self.execute_query(query)

    def get_temperature_trends(self, city_name: str = None) -> List[Dict[str, Any]]:
        """Get temperature trends over time."""
        query = """
        SELECT
            date,
            city,
            ROUND(temperature_high, 2) as temp_high,
            ROUND(temperature_low, 2) as temp_low,
            condition,
            humidity
        FROM weather_analytics
        ORDER BY city, date DESC
        LIMIT 30
        """
        return self.execute_query(query)

    def get_weather_condition_distribution(self) -> List[Dict[str, Any]]:
        """Get distribution of weather conditions."""
        query = """
        SELECT
            condition,
            COUNT(*) as count,
            ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) as percentage
        FROM weather_analytics
        GROUP BY condition
        ORDER BY count DESC
        """
        return self.execute_query(query)

    def get_extreme_weather_events(self) -> List[Dict[str, Any]]:
        """Identify extreme weather events."""
        query = """
        SELECT
            city,
            date,
            temperature_high,
            temperature_low,
            condition,
            humidity,
            wind_speed_kmh,
            precipitation_mm
        FROM weather_analytics
        WHERE temperature_high > 25 OR temperature_low < 0 OR wind_speed_kmh > 30
        ORDER BY date DESC
        LIMIT 20
        """
        return self.execute_query(query)

    def generate_analytics_report(self) -> Dict[str, Any]:
        """Generate complete analytics report."""
        self.connect()
        
        try:
            report = {
                "summary": self.get_weather_summary(),
                "city_temperatures": self.get_city_temperatures(),
                "weather_distribution": self.get_weather_condition_distribution(),
                "extreme_events": self.get_extreme_weather_events(),
            }
            logger.info("Analytics report generated successfully")
            return report
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {"error": str(e)}
        finally:
            self.disconnect()


def get_analytics_report() -> Dict[str, Any]:
    """Simple function to generate analytics report."""
    engine = AnalyticsQueryEngine()
    return engine.generate_analytics_report()

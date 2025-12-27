"""
Main orchestration script - runs the complete data lakehouse pipeline.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import ANALYTICS_DATA_PATH, TIMEZONE  # noqa: E402
from src.analytics.queries import AnalyticsQueryEngine  # noqa: E402
from src.ingestion.api_ingestion import APIIngestionManager  # noqa: E402
from src.ingestion.csv_ingestion import CSVIngestionManager  # noqa: E402
from src.transformations.clean_to_analytics import (  # noqa: E402
    CleanToAnalyticsTransformer,
)
from src.transformations.raw_to_clean import RawToCleanTransformer  # noqa: E402

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataLakehousePipeline:
    """Orchestrates the complete data lakehouse pipeline."""

    def __init__(self):
        self.start_time = datetime.now(TIMEZONE)
        self.execution_log = {
            "start_time": self.start_time.isoformat(),
            "stages": {},
        }

    def run_ingestion_stage(self) -> bool:
        """Run data ingestion from all sources."""
        logger.info("=" * 80)
        logger.info("STAGE 1: DATA INGESTION")
        logger.info("=" * 80)

        try:
            # API Ingestion
            logger.info("\n[1.1] Fetching data from OpenWeather API...")
            api_manager = APIIngestionManager()
            api_files = api_manager.ingest_all_cities()

            self.execution_log["stages"]["ingestion"] = {
                "api_files_ingested": len(api_files),
                "api_files": api_files,
            }

            logger.info(f"✓ Successfully ingested {len(api_files)} API files")

            # CSV Ingestion
            logger.info("\n[1.2] Ingesting CSV data...")
            csv_manager = CSVIngestionManager()

            # For demo, we'll use the sample CSV if it exists
            sample_csv = (
                Path(__file__).parent.parent
                / "data"
                / "raw"
                / "csv"
                / "sample_historical.csv"
            )
            if sample_csv.exists():
                success, path = csv_manager.ingest_csv(str(sample_csv))
                if success:
                    logger.info(f"✓ CSV ingestion successful: {path}")
                    self.execution_log["stages"]["ingestion"]["csv_files_ingested"] = 1
            else:
                logger.info("⊘ No sample CSV found for ingestion (optional)")
                self.execution_log["stages"]["ingestion"]["csv_files_ingested"] = 0

            return True

        except Exception as e:
            logger.error(f"✗ Ingestion stage failed: {str(e)}")
            self.execution_log["stages"]["ingestion"]["error"] = str(e)
            return False

    def run_transformation_stage(self) -> bool:
        """Run raw to clean transformation."""
        logger.info("\n" + "=" * 80)
        logger.info("STAGE 2: DATA TRANSFORMATION (RAW → CLEAN)")
        logger.info("=" * 80)

        try:
            transformer = RawToCleanTransformer()
            results = transformer.run_all_transformations()

            self.execution_log["stages"]["transformation"] = {
                "weather_files_transformed": len(results.get("weather_files", [])),
                "csv_files_transformed": len(results.get("csv_files", [])),
            }

            logger.info("✓ Transformation complete")
            logger.info(f"  - Weather files: {len(results['weather_files'])}")
            logger.info(f"  - CSV files: {len(results['csv_files'])}")

            return True

        except Exception as e:
            logger.error(f"✗ Transformation stage failed: {str(e)}")
            self.execution_log["stages"]["transformation"]["error"] = str(e)
            return False

    def run_analytics_stage(self) -> bool:
        """Run clean to analytics transformation and generate analytics."""
        logger.info("\n" + "=" * 80)
        logger.info("STAGE 3: ANALYTICS LAYER (CLEAN → ANALYTICS)")
        logger.info("=" * 80)

        try:
            # Load data into analytical tables
            logger.info("\n[3.1] Creating analytical tables in DuckDB...")
            transformer = CleanToAnalyticsTransformer()
            transform_result = transformer.run_all_transformations()

            if transform_result.get("status") == "success":
                logger.info("✓ Analytical tables created successfully")
                logger.info(
                    f"  - Exported files: {len(transform_result.get('exported_files', []))}"
                )

                # Generate analytics report
                logger.info("\n[3.2] Generating analytics report...")
                query_engine = AnalyticsQueryEngine()
                report = query_engine.generate_analytics_report()

                # Save report to file
                report_path = ANALYTICS_DATA_PATH / "analytics_report.json"
                with open(report_path, "w") as f:
                    json.dump(report, f, indent=2, default=str)

                logger.info(f"✓ Analytics report saved: {report_path}")

                # Display summary
                summary = report.get("summary", {})
                if summary:
                    logger.info("\n[Analytics Summary]")
                    logger.info(
                        f"  Cities loaded: {len(summary.get('cities_loaded', []))}"
                    )
                    logger.info(
                        f"  Total records: {summary.get('weather_analytics_rows', 0)}"
                    )

                self.execution_log["stages"]["analytics"] = {
                    "status": "success",
                    "report_path": str(report_path),
                    "summary": summary,
                }
            else:
                logger.warning(
                    "⊘ Analytics tables not created (likely no clean data available)"
                )
                self.execution_log["stages"]["analytics"] = {"status": "no_data"}

            return True

        except Exception as e:
            logger.error(f"✗ Analytics stage failed: {str(e)}")
            self.execution_log["stages"]["analytics"]["error"] = str(e)
            return False

    def print_execution_summary(self):
        """Print execution summary."""
        end_time = datetime.now(TIMEZONE)
        duration = (end_time - self.start_time).total_seconds()

        logger.info("\n" + "=" * 80)
        logger.info("PIPELINE EXECUTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Start time: {self.start_time.isoformat()}")
        logger.info(f"End time: {end_time.isoformat()}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info("\nData Lakehouse Layers:")
        logger.info("  ✓ Raw Layer: Data ingested from API and CSV sources")
        logger.info("  ✓ Clean Layer: Data normalized and flattened")
        logger.info("  ✓ Analytics Layer: Data models created for analysis")
        logger.info("\nNext steps:")
        logger.info(
            "  1. Review the data in each layer: data/raw, data/clean, data/analytics"
        )
        logger.info("  2. Query the DuckDB database: data/analytics/lakehouse.duckdb")
        logger.info(
            "  3. Check the analytics report: data/analytics/analytics_report.json"
        )
        logger.info("=" * 80)

    def run(self) -> bool:
        """Run the complete pipeline."""
        logger.info("Starting Data Lakehouse Simulation Pipeline...")
        logger.info(f"Execution time: {self.start_time.isoformat()}")

        stages_successful = []

        # Run each stage
        stages_successful.append(("Ingestion", self.run_ingestion_stage()))
        stages_successful.append(("Transformation", self.run_transformation_stage()))
        stages_successful.append(("Analytics", self.run_analytics_stage()))

        # Summary
        self.print_execution_summary()

        # Save execution log
        self.execution_log["end_time"] = datetime.now(TIMEZONE).isoformat()
        log_path = ANALYTICS_DATA_PATH / "execution_log.json"
        with open(log_path, "w") as f:
            json.dump(self.execution_log, f, indent=2, default=str)

        logger.info(f"\nExecution log saved: {log_path}")

        # Check if all critical stages succeeded
        return all(
            success for _, success in stages_successful[:2]
        )  # At least ingestion and transformation


if __name__ == "__main__":
    pipeline = DataLakehousePipeline()
    success = pipeline.run()

    sys.exit(0 if success else 1)

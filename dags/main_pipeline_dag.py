"""
Main Data Lakehouse Pipeline DAG
Orchestrates the complete ETL pipeline: Ingestion → Transformation → Analytics
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.run_pipeline import DataLakehousePipeline  # noqa: E402


def run_ingestion():
    """Execute data ingestion stage."""
    pipeline = DataLakehousePipeline()
    pipeline.run_ingestion_stage()


def run_transformation():
    """Execute data transformation stage."""
    pipeline = DataLakehousePipeline()
    pipeline.run_transformation_stage()


def run_analytics():
    """Execute analytics stage."""
    pipeline = DataLakehousePipeline()
    pipeline.run_analytics_stage()


# DAG configuration
default_args = {
    "owner": "data-engineer",
    "description": "Data Lakehouse ETL Pipeline",
    "start_date": datetime(2025, 12, 22),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
}

# Define DAG
dag = DAG(
    "data_lakehouse_pipeline",
    default_args=default_args,
    description="Complete lakehouse ETL: Ingest → Transform → Analyze",
    schedule_interval="0 2 * * *",  # Daily at 2:00 AM UTC
    catchup=False,
    tags=["data-engineering", "lakehouse", "etl"],
)

# Define tasks
with dag:
    # Task group for data ingestion
    with TaskGroup("ingestion_stage") as ingestion_group:
        ingest_task = PythonOperator(
            task_id="fetch_and_ingest_data",
            python_callable=run_ingestion,
            doc="Fetch weather data from API and CSV files",
        )

    # Task group for transformation
    with TaskGroup("transformation_stage") as transformation_group:
        transform_task = PythonOperator(
            task_id="normalize_and_clean_data",
            python_callable=run_transformation,
            doc="Normalize and flatten data from raw to clean layer",
        )

    # Task group for analytics
    with TaskGroup("analytics_stage") as analytics_group:
        analytics_task = PythonOperator(
            task_id="create_analytics_tables",
            python_callable=run_analytics,
            doc="Create DuckDB tables and generate analytics report",
        )

    # Health check
    health_check = BashOperator(
        task_id="verify_output",
        bash_command='test -f {{ params.output_file }} && echo "Pipeline successful" || echo "Pipeline failed"',
        params={
            "output_file": str(
                project_root / "data" / "analytics" / "analytics_report.json"
            )
        },
    )

    # Define dependencies
    ingestion_group >> transformation_group >> analytics_group >> health_check


if __name__ == "__main__":
    print(f"DAG: {dag.dag_id}")
    print(f"Schedule: {dag.schedule_interval}")
    print(f"Start Date: {dag.start_date}")

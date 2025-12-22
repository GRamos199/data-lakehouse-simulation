"""
Sample Data Generation DAG
Generates new sample weather data for pipeline testing
Useful for development and testing without waiting for real API data
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.generate_sample_data import generate_sample_csv


def generate_new_sample_data():
    """Generate fresh sample data for testing."""
    generate_sample_csv()
    return "Sample data generated successfully"


# DAG configuration
default_args = {
    'owner': 'data-engineer',
    'description': 'Generate sample data for testing',
    'start_date': datetime(2025, 12, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# Define DAG
dag = DAG(
    'data_generation_pipeline',
    default_args=default_args,
    description='Generate sample weather data for testing',
    schedule_interval='0 0 * * 0',  # Weekly on Sunday at midnight
    catchup=False,
    tags=['data-generation', 'testing'],
)

# Define tasks
with dag:
    generate_data = PythonOperator(
        task_id='generate_sample_data',
        python_callable=generate_new_sample_data,
        doc='Generate 150 random weather records across 5 cities'
    )
    
    generate_data


if __name__ == '__main__':
    print(f"DAG: {dag.dag_id}")
    print(f"Schedule: {dag.schedule_interval}")

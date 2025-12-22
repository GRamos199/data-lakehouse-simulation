# Data Lakehouse - Airflow Architecture

## Overview

The Data Lakehouse uses Apache Airflow for orchestrating and scheduling the ETL pipeline. This document explains the architecture.

## DAG Structure

### Main Pipeline DAG
**File**: `dags/main_pipeline_dag.py`
**Schedule**: Daily at 2:00 AM UTC
**Duration**: ~2-5 seconds

```
data_lakehouse_pipeline
│
├── ingestion_stage
│   └── fetch_and_ingest_data (PythonOperator)
│
├── transformation_stage  
│   └── normalize_and_clean_data (PythonOperator)
│
├── analytics_stage
│   └── create_analytics_tables (PythonOperator)
│
└── verify_output (BashOperator)
    └── Check if analytics_report.json exists
```

**Task Groups**: Organize related tasks logically
- `ingestion_stage` - Data ingestion tasks
- `transformation_stage` - Data cleaning tasks
- `analytics_stage` - Analytics tasks

### Data Generation DAG
**File**: `dags/data_generation_dag.py`
**Schedule**: Weekly on Sunday at midnight UTC
**Duration**: ~1 second

```
data_generation_pipeline
│
└── generate_sample_data (PythonOperator)
    └── Creates 150 sample weather records
```

## Execution Flow

### Option 1: Manual Execution
```bash
python3 scripts/run_pipeline.py
```
Single execution, no scheduling.

### Option 2: Scheduled with Airflow
```bash
# Setup
bash scripts/setup_airflow.sh

# Terminal 1: Webserver
airflow webserver -p 8080

# Terminal 2: Scheduler
airflow scheduler
```

The scheduler automatically runs DAGs based on their `schedule_interval`.

## Configuration

### Airflow Config (`airflow.cfg`)
- **Executor**: LocalExecutor (single machine)
- **Backend**: SQLite (airflow_home/airflow.db)
- **DAGs Folder**: dags/
- **Max Parallelism**: 4 tasks
- **Max Active Runs**: 1 per DAG

### DAG Parameters
Each DAG has:
- `default_args` - Owner, retries, error handling
- `schedule_interval` - When to run (cron format)
- `catchup=False` - Don't backfill old dates
- `tags` - For organizing DAGs in UI

## Task Dependencies

Tasks are organized with `>>` operator:
```python
ingestion_group >> transformation_group >> analytics_group >> health_check
```

This ensures:
1. Ingestion runs first
2. Transformation waits for ingestion to complete
3. Analytics waits for transformation
4. Health check runs last

## Monitoring

### Web UI (http://localhost:8080)
- **DAGs List**: View all DAGs
- **Runs**: See execution history
- **Task Instances**: Check individual task status
- **Logs**: View detailed task output
- **Calendar**: Historical view of runs

### Key Metrics
- **Total Runs**: How many times DAG executed
- **Failed Runs**: How many failed
- **Success Rate**: % of successful runs
- **Average Duration**: How long each run takes

## Scaling Considerations

### Current (LocalExecutor)
- Runs on single machine
- Sequential task execution
- Good for development & testing
- Up to 4 concurrent tasks

### Future (CeleryExecutor)
For production scaling:
- Distributed task execution
- Multiple worker nodes
- RabbitMQ/Redis as message broker
- Horizontal scaling

### Current Configuration Limits
- Max 4 parallel tasks: `parallelism = 4`
- Max 8 active tasks per DAG: `max_active_tasks_per_dag = 8`
- Max 1 run per DAG: `max_active_runs_per_dag = 1`

## Error Handling

### Retry Logic
```python
default_args = {
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}
```

If a task fails:
1. Wait 5 minutes
2. Retry up to 2 times
3. If still fails, mark as Failed

### Task Status
- **Success**: Task completed successfully
- **Failed**: Task failed after retries
- **Upstream Failed**: A dependency failed
- **Skipped**: Task was skipped
- **Running**: Task currently executing

## Data Flow in Airflow

```
Schedule Trigger (2 AM UTC)
    ↓
Scheduler activates DAG run
    ↓
Task 1: Ingestion
    ├─ Fetch from OpenWeather API
    └─ Read CSV files
    ↓
Task 2: Transformation
    ├─ Normalize data
    └─ Create clean CSVs
    ↓
Task 3: Analytics
    ├─ Create DuckDB tables
    └─ Generate report
    ↓
Task 4: Health Check
    └─ Verify output files exist
    ↓
DAG Run Marked as Success/Failed
    ↓
Logs saved to airflow_home/logs/
    ↓
Next scheduled run (24 hours later)
```

## Adding New Tasks

### Simple Python Task
```python
from airflow.operators.python import PythonOperator

def my_function():
    print("Task executed!")

task = PythonOperator(
    task_id='my_task',
    python_callable=my_function,
    dag=dag,
)
```

### Task Group
```python
from airflow.utils.task_group import TaskGroup

with TaskGroup('my_group') as tg:
    task1 = PythonOperator(...)
    task2 = PythonOperator(...)
    task1 >> task2
```

### Adding to DAG
```python
ingestion_group >> my_new_task >> transformation_group
```

## Key Files

| File | Purpose |
|------|---------|
| `dags/main_pipeline_dag.py` | Main ETL orchestration |
| `dags/data_generation_dag.py` | Weekly data generation |
| `airflow.cfg` | Airflow configuration |
| `scripts/setup_airflow.sh` | Initialization script |
| `AIRFLOW_GUIDE.md` | Detailed usage guide |

## Environment Variables

Airflow reads from `.env` for API keys:
```bash
export OPENWEATHER_API_KEY="bd737af049f9ef0682209ea1be369eea"
```

The config.py loads this automatically using python-dotenv.

## Performance

### Current Metrics
- Ingestion: ~1.5 seconds (5 API calls)
- Transformation: ~0.1 seconds (CSV processing)
- Analytics: ~1 second (DuckDB operations)
- Total: ~2.6 seconds per run

### Optimization Tips
1. Cache API responses
2. Batch process CSV files
3. Use DuckDB streaming
4. Parallelize city processing

## Debugging

### Enable Debug Logging
```bash
export AIRFLOW__CORE__UNIT_TEST_MODE=False
export AIRFLOW__LOGGING__LOGGING_LEVEL=DEBUG
airflow scheduler
```

### Test a DAG
```bash
airflow dags test data_lakehouse_pipeline 2025-12-22
```

### Check Task Dependencies
```bash
airflow tasks list data_lakehouse_pipeline --tree
```

### View Logs
```bash
tail -f airflow_home/logs/*/
```

## Next Steps

1. **Add more DAGs** for additional pipelines
2. **Integrate with data warehouse** (Snowflake, BigQuery)
3. **Add SLA monitoring** for SLA compliance
4. **Set up alerting** for failures
5. **Scale with CeleryExecutor** for distributed execution
6. **Implement data quality checks** with Great Expectations

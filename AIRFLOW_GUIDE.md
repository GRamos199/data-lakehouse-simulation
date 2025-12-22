# Apache Airflow Setup & Scheduler Guide

This document explains how to set up and run the Data Lakehouse Pipeline with Apache Airflow for automated, scheduled execution.

## Why Airflow?

Apache Airflow provides:
- **Scheduling** - Execute pipeline on a fixed schedule (daily, weekly, etc.)
- **Monitoring** - Web UI to track DAG runs and task status
- **Retry Logic** - Automatic retries on failure
- **Task Dependency** - Ensure tasks run in correct order
- **Logging** - Detailed logs for debugging

## Quick Setup

### 1. Initialize Airflow

```bash
bash scripts/setup_airflow.sh
```

This script will:
- Install Apache Airflow dependencies
- Create Airflow directories
- Initialize the SQLite database
- Create an admin user (admin/admin)
- Enable both DAGs

### 2. Start the Webserver

```bash
airflow webserver -p 8080
```

Access at: http://localhost:8080

### 3. Start the Scheduler (in another terminal)

```bash
airflow scheduler
```

The scheduler monitors DAGs and triggers runs based on the schedule.

## Available DAGs

### `data_lakehouse_pipeline`
- **Schedule**: Daily at 2:00 AM UTC
- **Duration**: ~2-5 seconds per run
- **Tasks**:
  - `ingestion_stage` - Fetch API and CSV data
  - `transformation_stage` - Normalize and flatten
  - `analytics_stage` - Create tables and generate report
  - `verify_output` - Health check

### `data_generation_pipeline`
- **Schedule**: Weekly on Sunday at midnight UTC
- **Duration**: ~1 second
- **Purpose**: Generate fresh test data automatically
- **Task**:
  - `generate_sample_data` - Create 150 sample weather records

## Using the Web UI

### Access Dashboard
1. Open: http://localhost:8080
2. Login: admin / admin
3. View all DAGs and their status

### Trigger a DAG Manually
1. Click the DAG name
2. Click "Trigger DAG" button
3. Watch the run in real-time

### View Logs
1. Click on a task in a DAG run
2. Click "Log" tab to see detailed execution logs

### Monitor Performance
- **Runs**: View execution history
- **Tree View**: Visualize task dependencies
- **Graph View**: See task relationships
- **Calendar**: View historical success/failure

## CLI Commands

### View DAGs
```bash
airflow dags list
airflow dags list -o plain
```

### Trigger DAG Manually
```bash
airflow dags trigger data_lakehouse_pipeline
```

### Check DAG Status
```bash
airflow dags test data_lakehouse_pipeline
```

### View Task List
```bash
airflow tasks list data_lakehouse_pipeline
```

### View Execution History
```bash
airflow dags list-runs -d data_lakehouse_pipeline
```

### Enable/Disable DAG
```bash
airflow dags unpause data_lakehouse_pipeline
airflow dags pause data_lakehouse_pipeline
```

## Customizing Schedules

Edit `dags/main_pipeline_dag.py` to change the schedule:

```python
schedule_interval='0 2 * * *',  # Daily at 2:00 AM UTC

# Other examples:
# '0 * * * *'       - Every hour
# '0 0 * * *'       - Daily at midnight
# '0 0 * * 0'       - Weekly on Sunday
# '0 0 1 * *'       - Monthly on 1st
# None              - Manual trigger only
```

Cron format: `minute hour day month day_of_week`

## Database Management

### View Database
```bash
sqlite3 airflow_home/airflow.db
```

### Reset Database (WARNING: Clears all history)
```bash
rm airflow_home/airflow.db
airflow db init
airflow users create --username admin --password admin
```

## Monitoring & Alerts

### Check Airflow Health
```bash
airflow config list
airflow version
```

### View Recent Task Failures
```bash
airflow tasks failed-deps data_lakehouse_pipeline
```

### Email Alerts (Optional)
Set up in `airflow.cfg`:
```ini
[email]
email_backend = airflow.providers.smtp.utils.smtp_mail_backend

[smtp]
smtp_host = smtp.gmail.com
smtp_port = 587
smtp_user = your-email@gmail.com
smtp_password = your-app-password
```

Then in DAG:
```python
default_args = {
    'email': ['your-email@example.com'],
    'email_on_failure': True,
}
```

## Troubleshooting

### DAGs not appearing
1. Check `dags` folder exists and has DAG files
2. Restart scheduler: `airflow scheduler`
3. Check logs: `cat airflow_home/logs/scheduler.log`

### Task fails consistently
1. View logs: Click task → Log tab
2. Check if dependencies are installed: `pip list | grep apache-airflow`
3. Verify Python path: `python scripts/run_pipeline.py` (run manually)

### Webserver won't start
1. Check port 8080 is not in use: `lsof -i :8080`
2. Kill existing process: `pkill -f 'airflow webserver'`
3. Delete lock file: `rm airflow_home/webserver.pid`

### Scheduler not running tasks
1. Check scheduler is running: `ps aux | grep scheduler`
2. Verify DAG is unpaused: `airflow dags list` (look for state)
3. Check system time is correct: `date`

## Production Considerations

For production deployment:

1. **Use PostgreSQL** instead of SQLite
2. **Use CeleryExecutor** for distributed execution
3. **Set up monitoring** (Prometheus, DataDog)
4. **Configure email alerts**
5. **Change secret key** in `airflow.cfg`
6. **Use environment variables** for sensitive config
7. **Set up backups** for database
8. **Monitor logs** and task failures

## Example: Adding a New DAG

Create `dags/my_new_dag.py`:

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def my_task():
    print("Task executed!")

dag = DAG(
    'my_new_dag',
    start_date=datetime(2025, 12, 22),
    schedule_interval='0 3 * * *',  # 3 AM daily
    catchup=False,
    tags=['custom'],
)

task = PythonOperator(
    task_id='my_task',
    python_callable=my_task,
    dag=dag,
)
```

The DAG will auto-load within 5 minutes!

## Resources

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Best Practices](https://airflow.apache.org/docs/stable/best-practices.html)
- [Cron Syntax](https://crontab.guru/)

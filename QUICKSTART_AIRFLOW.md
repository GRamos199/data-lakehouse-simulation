# ⚡ Quick Start - Apache Airflow

## Installation (30 seconds)

```bash
bash scripts/setup_airflow.sh
```

This will:
- ✅ Install Apache Airflow 2.7.3
- ✅ Initialize SQLite database
- ✅ Create admin user (admin/admin)
- ✅ Enable both DAGs

## Start Services (2 terminals)

**Terminal 1 - Webserver**
```bash
airflow webserver -p 8080
```

**Terminal 2 - Scheduler**
```bash
airflow scheduler
```

Then access: **http://localhost:8080**

## Available DAGs

| DAG | Schedule | Purpose |
|-----|----------|---------|
| `data_lakehouse_pipeline` | Daily @ 2 AM UTC | Full ETL |
| `data_generation_pipeline` | Weekly Sunday | Test data |

## Common Commands

```bash
# List all DAGs
airflow dags list

# Trigger manually
airflow dags trigger data_lakehouse_pipeline

# Check status
airflow dags test data_lakehouse_pipeline

# View logs
airflow logs list

# Unpause DAG
airflow dags unpause data_lakehouse_pipeline
```

## Manual Alternative

Skip Airflow and run directly:
```bash
python3 scripts/run_pipeline.py
```

## Troubleshooting

**Port 8080 in use?**
```bash
pkill -f 'airflow webserver'
```

**Reset everything:**
```bash
rm -rf airflow_home/
bash scripts/setup_airflow.sh
```

## Documentation

- [README.md](README.md) - Project overview
- [AIRFLOW_GUIDE.md](AIRFLOW_GUIDE.md) - Detailed guide
- [AIRFLOW_ARCHITECTURE.md](AIRFLOW_ARCHITECTURE.md) - Architecture details

---

**That's it! Airflow is ready to automate your data pipeline.** 🚀

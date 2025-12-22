#!/bin/bash
# Setup and initialize Apache Airflow for Data Lakehouse Pipeline

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AIRFLOW_HOME="$PROJECT_ROOT/airflow_home"
VENV_PATH="$PROJECT_ROOT/venv"

echo "=================================================="
echo "Data Lakehouse - Apache Airflow Setup"
echo "=================================================="
echo ""

# Check if venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at $VENV_PATH"
    echo "   Please run: python3 -m venv venv && source venv/bin/activate"
    exit 1
fi

# Activate venv
echo "📦 Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Install/upgrade Airflow
echo "📥 Installing Apache Airflow..."
pip install -q apache-airflow==2.7.3 apache-airflow-providers-python==4.4.0

# Create Airflow home directory
echo "📁 Setting up Airflow directories..."
mkdir -p "$AIRFLOW_HOME"/{dags,logs,plugins}

# Set Airflow environment variables
export AIRFLOW_HOME="$AIRFLOW_HOME"
export AIRFLOW__CORE__DAGS_FOLDER="$PROJECT_ROOT/dags"
export AIRFLOW__CORE__BASE_LOG_FOLDER="$AIRFLOW_HOME/logs"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN="sqlite:///$AIRFLOW_HOME/airflow.db"
export AIRFLOW__CORE__LOAD_EXAMPLES="False"
export AIRFLOW__WEBSERVER__SECRET_KEY="data-lakehouse-secret-key"

# Initialize Airflow database
echo "🗄️  Initializing Airflow database..."
airflow db init

# Create default admin user
echo "👤 Creating admin user..."
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@localhost.localdomain \
    --password admin \
    2>/dev/null || echo "   Admin user already exists"

# Unpause DAGs
echo "▶️  Enabling DAGs..."
airflow dags unpause data_lakehouse_pipeline 2>/dev/null || true
airflow dags unpause data_generation_pipeline 2>/dev/null || true

# Display information
echo ""
echo "=================================================="
echo "✅ Airflow setup complete!"
echo "=================================================="
echo ""
echo "📊 Webserver access:"
echo "   Command: airflow webserver -p 8080"
echo "   URL: http://localhost:8080"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "⚙️  Scheduler:"
echo "   Command: airflow scheduler"
echo ""
echo "📝 DAGs location: $PROJECT_ROOT/dags"
echo "🗂️  Airflow home: $AIRFLOW_HOME"
echo ""
echo "To start developing:"
echo "1. Terminal 1: airflow webserver -p 8080"
echo "2. Terminal 2: airflow scheduler"
echo "3. Access: http://localhost:8080"
echo ""

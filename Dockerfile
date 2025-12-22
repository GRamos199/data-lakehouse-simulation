FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    AIRFLOW_HOME=/airflow \
    AIRFLOW__CORE__DAGS_FOLDER=/airflow/dags \
    AIRFLOW__CORE__LOAD_EXAMPLES=False \
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:////airflow/airflow.db

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create Airflow directory
RUN mkdir -p /airflow /app

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app/

WORKDIR /app

# Expose Airflow webserver port
EXPOSE 8081

# Create Airflow user and initialize database
RUN airflow db migrate && \
    airflow users create --username admin --password admin \
    --firstname Admin --lastname User --role Admin \
    --email admin@example.com || true

CMD ["bash", "-c", "airflow webserver -p 8081 & airflow scheduler"]

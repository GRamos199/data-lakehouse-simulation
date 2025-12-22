# 🎯 Resumen Ejecutivo: Airflow + Data Lakehouse

## ¿QUÉ ES AIRFLOW?

Imagina que tienes una fábrica de datos. **Airflow es el gerente de la fábrica** que:
- ⏰ Supervisa que todo ocurra en el horario correcto
- 🔄 Reinicia automáticamente si algo falla
- 📊 Te muestra reportes de lo que sucedió
- 🚨 Te alerta si hay problemas

## ¿CUÁNDO EJECUTA EL PIPELINE?

```
Todos los DÍAS a las 2:00 AM UTC (10 PM EDT)
  ↓
  Extrae datos del API de OpenWeather
  ↓
  Limpia y normaliza los datos
  ↓
  Crea tablas analíticas con agregados
  ↓
  Genera reporte JSON
  ↓
  ✓ Completado (o ✗ Fallido → Reintentos automáticos)
```

## ¿DÓNDE GUARDA LOS DATOS?

### En el CONTENEDOR DOCKER (no en tu PC):

```
Contenedor: data-lakehouse-airflow
├── /app/data/
│   ├── raw/api/              ← Respuestas JSON del API (JSON crudos)
│   ├── raw/csv/              ← CSVs importados (sin procesar)
│   ├── clean/                ← Datos limpios (Parquet)
│   └── analytics/            ← Base de datos DuckDB (vistas SQL)
└── /app/outputs/
    └── analytics_report.json ← Reporte final (JSON)
```

### En tu PC (sincroniazado):

```
/home/george/data-lakehouse-simulation/
├── data/                     ← Se sincroniza automáticamente
├── outputs/                  ← Se sincroniza automáticamente
└── logs/                     ← Logs de Airflow
```

## DATOS REALES DE EJEMPLO

### Entrada (API):
```json
{
  "city": "London",
  "date": "2025-12-22",
  "temperature_celsius": 5.2,
  "humidity_percent": 78,
  "wind_speed_kmh": 12.5
}
```

### Salida (Analytics Report):
```json
{
  "timestamp": "2025-12-22T14:00:00Z",
  "total_records": 150,
  "cities": ["London", "Tokyo", "New York", "Los Angeles", "Sydney"],
  "temperature_stats": {
    "average": 18.5,
    "max": 35.2,
    "min": -2.1
  },
  "execution_time_seconds": 45,
  "status": "SUCCESS"
}
```

## 3 FORMAS DE EJECUTAR

### 1️⃣ AUTOMÁTICAMEN (Recomendado)
- Airflow ejecuta automáticamente cada día a las 2 AM UTC
- Todo ocurre en background (Docker)
- Monitoreas desde Web UI: http://localhost:8081

### 2️⃣ MANUAL VIA WEB UI
1. Abre http://localhost:8081
2. Busca `data_lakehouse_pipeline`
3. Clickea el botón de play (▶)
4. Ve en vivo cómo se ejecuta

### 3️⃣ MANUAL VIA TERMINAL
```bash
docker exec data-lakehouse-airflow \
  airflow dags trigger data_lakehouse_pipeline
```

## MONITOREO EN TIEMPO REAL

### Web UI (http://localhost:8081)
- **Dashboard**: Ve estado de todos los DAGs
- **DAGs**: Visualiza el flujo gráfico
- **Grid**: Historial de todas las ejecuciones
- **Logs**: Lee logs detallados de cada tarea

### Terminal (Logs en vivo)
```bash
docker logs -f data-lakehouse-airflow 2>&1 | grep -E "STAGE|✓|✗"
```

## LOGS ESPERADOS (EJEMPLO)

```
2025-12-22 14:00:00 - ================================================
2025-12-22 14:00:00 - STAGE 1: DATA INGESTION
2025-12-22 14:00:00 - ================================================
2025-12-22 14:00:01 - [1.1] Fetching data from OpenWeather API...
2025-12-22 14:00:02 - ✓ API Request: London - Status 200 - 150 records
2025-12-22 14:00:03 - ✓ Saved: /data/raw/api/london_2025-12-22.json
2025-12-22 14:00:04 - ✓ API Request: Tokyo - Status 200 - 155 records
2025-12-22 14:00:05 - ✓ Saved: /data/raw/api/tokyo_2025-12-22.json
2025-12-22 14:00:10 - ✓ Successfully ingested 5 API files (750 total records)
2025-12-22 14:00:11 - ================================================
2025-12-22 14:00:11 - STAGE 2: TRANSFORMATION
2025-12-22 14:00:11 - ================================================
2025-12-22 14:00:12 - [2.1] Loading raw data...
2025-12-22 14:00:13 - Loaded 5 JSON files from API (750 records)
2025-12-22 14:00:14 - [2.2] Normalizing and cleaning data...
2025-12-22 14:00:15 - ✓ Removed 0 duplicate records
2025-12-22 14:00:16 - ✓ Handled missing values
2025-12-22 14:00:17 - ✓ Standardized datetime formats
2025-12-22 14:00:18 - [2.3] Saving cleaned data...
2025-12-22 14:00:20 - ✓ Saved: /data/clean/2025-12-22_merged_clean.parquet
2025-12-22 14:00:21 - ================================================
2025-12-22 14:00:21 - STAGE 3: ANALYTICS
2025-12-22 14:00:21 - ================================================
2025-12-22 14:00:22 - [3.1] Loading clean data...
2025-12-22 14:00:23 - Loaded 750 records from parquet
2025-12-22 14:00:24 - [3.2] Creating analytics views...
2025-12-22 14:00:25 - ✓ Created VIEW: temperature_stats
2025-12-22 14:00:26 - ✓ Created VIEW: city_weather_summary
2025-12-22 14:00:27 - ✓ Created VIEW: daily_aggregates
2025-12-22 14:00:28 - [3.3] Generating report...
2025-12-22 14:00:30 - ✓ Saved: /outputs/analytics_report.json
2025-12-22 14:00:31 - ================================================
2025-12-22 14:00:31 - HEALTH CHECK
2025-12-22 14:00:31 - ================================================
2025-12-22 14:00:32 - ✓ Analytics report found and validated
2025-12-22 14:00:33 - ✓ PIPELINE EXECUTION SUCCESSFUL
2025-12-22 14:00:33 - Total execution time: 33 seconds
```

## ESTRUCTURA DE DATOS

```
Raw Layer (JSON API)
    ↓ (150 registros × 5 ciudades = 750 filas)
    
    london_2025-12-22.json
    tokyo_2025-12-22.json
    new_york_2025-12-22.json
    los_angeles_2025-12-22.json
    sydney_2025-12-22.json

            ↓↓↓ TRANSFORMATION ↓↓↓

Clean Layer (Parquet)
    ↓ (750 registros, limpios y normalizados)
    
    2025-12-22_merged_clean.parquet
    - Sin duplicados
    - Fechas normalizadas
    - Valores validados

            ↓↓↓ ANALYTICS ↓↓↓

Analytics Layer (DuckDB)
    ↓ (Vistas SQL agregadas)
    
    temperature_stats:
    - city: London, avg_temp: 5.2, max: 12.1, min: -2.0
    - city: Tokyo, avg_temp: 8.5, max: 15.3, min: 2.1
    ... etc
    
    city_weather_summary:
    - city: London, total_records: 150, avg_humidity: 78%
    - city: Tokyo, total_records: 150, avg_humidity: 65%
    ... etc

            ↓↓↓ FINAL REPORT ↓↓↓

Output (JSON)
    ↓
    analytics_report.json
    {
      "timestamp": "2025-12-22T14:00:00Z",
      "total_records": 750,
      "cities": 5,
      "temperature_avg": 18.5,
      "execution_time_seconds": 33,
      "status": "SUCCESS"
    }
```

## PRÓXIMAS EJECUCIONES PROGRAMADAS

| DAG | Próxima Ejecución | Frecuencia |
|-----|------------------|-----------|
| `data_lakehouse_pipeline` | Mañana 2:00 AM UTC | Diariamente |
| `data_generation_pipeline` | Este domingo | Semanalmente |

---

## 🔗 REFERENCIAS RÁPIDAS

- **Web UI**: http://localhost:8081 (admin/admin)
- **Documentación detallada**: `AIRFLOW_EXECUTION_GUIDE.md`
- **Ver logs en vivo**: `docker logs -f data-lakehouse-airflow`
- **Ejecutar manualmente**: `docker exec data-lakehouse-airflow airflow dags trigger data_lakehouse_pipeline`

---

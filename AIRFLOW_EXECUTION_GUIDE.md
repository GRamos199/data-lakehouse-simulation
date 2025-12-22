# 🚀 Guía de Ejecución y Logging del Pipeline Airflow

## ¿Qué hace Airflow en este proyecto?

**Apache Airflow** es un orquestador de workflows que automatiza la ejecución del pipeline de datos en horarios programados.

### Funciones principales:

```
┌─────────────────────────────────────────────────────────────┐
│              APACHE AIRFLOW SCHEDULER                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ⏰ SCHEDULER (Ejecuta en background)                       │
│   └─ Monitorea los DAGs cada 5 minutos                      │
│   └─ Ejecuta tareas según el cronograma configurado         │
│   └─ Reintentar automáticamente si falla (2 intentos)      │
│   └─ Registra logs detallados de cada ejecución             │
│                                                              │
│  🌐 WEB UI (Puerto 8081)                                    │
│   └─ Visualiza DAGs disponibles                             │
│   └─ Monitorea ejecuciones en tiempo real                   │
│   └─ Ve logs de cada tarea                                  │
│   └─ Ejecuta DAGs manualmente si lo deseas                  │
│                                                              │
│  📊 DATABASE (SQLite)                                       │
│   └─ Almacena metadata de ejecuciones                       │
│   └─ Registra estado de tareas (success/failed)             │
│   └─ Guarda histórico de ejecutios                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📅 Cronograma de Ejecuciones

### DAG: `data_lakehouse_pipeline` (Principal)
- **Horario**: Diariamente a las **2:00 AM UTC** (10:00 PM EDT)
- **Frecuencia**: Todos los días
- **Duración estimada**: 30-60 segundos
- **Reintentos**: 2 intentos con 5 minutos de espera

**Estructura de tareas**:
```
ingestion_stage
    ↓
transformation_stage
    ↓
analytics_stage
    ↓
health_check (verifica que todo está OK)
```

### DAG: `data_generation_pipeline` (Generador de datos)
- **Horario**: Domingos a **00:00 UTC** (8:00 PM sábado EDT)
- **Frecuencia**: Una vez por semana
- **Duración estimada**: 5-10 segundos
- **Propósito**: Generar datos de prueba frescos

---

## 📂 Ubicación de Datos Extraídos

### Estructura de directorios:

```
/home/george/data-lakehouse-simulation/
├── data/
│   ├── raw/                          # 🔴 CAPA RAW (Datos sin procesar)
│   │   ├── api/                      
│   │   │   ├── london_2025-12-22.json    # API OpenWeather JSON
│   │   │   ├── tokyo_2025-12-22.json
│   │   │   ├── new_york_2025-12-22.json
│   │   │   ├── los_angeles_2025-12-22.json
│   │   │   └── sydney_2025-12-22.json
│   │   └── csv/
│   │       └── sample_historical.csv     # Datos históricos CSV
│   │
│   ├── clean/                        # 🟢 CAPA CLEAN (Datos normalizados)
│   │   └── 2025-12-22_merged_clean.parquet
│   │
│   └── analytics/                    # 🔵 CAPA ANALYTICS (Agregados)
│       ├── analytics.db              # DuckDB con vistas analíticas
│       └── reports/
│           └── analytics_report.json # Reporte JSON final
│
├── outputs/                          # Resultados finales
│   └── analytics_report.json         # Mismo que arriba (copia)
│
├── logs/                             # Logs de Airflow
│   └── data_lakehouse_pipeline/
│       ├── ingestion_stage/
│       ├── transformation_stage/
│       ├── analytics_stage/
│       └── health_check/
│
└── airflow_home/
    ├── airflow.db                    # Database SQLite de Airflow
    └── logs/                         # Logs de ejecución
```

---

## 🔍 Proceso Detallado de Extracción (Con Logs)

### **STAGE 1: INGESTION** (Extracción)

Airflow ejecuta:
```python
python3 scripts/run_pipeline.py  # Función: run_ingestion_stage()
```

**Logs esperados**:
```
[2025-12-22 14:00:00] INFO - ===============================================
[2025-12-22 14:00:00] INFO - STAGE 1: DATA INGESTION
[2025-12-22 14:00:00] INFO - ===============================================
[2025-12-22 14:00:01] INFO - [1.1] Fetching data from OpenWeather API...
[2025-12-22 14:00:02] INFO - ✓ API Request: London - Status 200
[2025-12-22 14:00:03] INFO - ✓ Saved: /data/raw/api/london_2025-12-22.json
[2025-12-22 14:00:04] INFO - ✓ API Request: Tokyo - Status 200
[2025-12-22 14:00:05] INFO - ✓ Saved: /data/raw/api/tokyo_2025-12-22.json
...
[2025-12-22 14:00:15] INFO - ✓ Successfully ingested 5 API files
[2025-12-22 14:00:16] INFO - [1.2] Ingesting CSV data...
[2025-12-22 14:00:17] INFO - ✓ CSV ingestion successful
```

**¿Qué sucede?**:
1. Conecta a OpenWeather API con tu clave
2. Obtiene datos de 5 ciudades (London, Tokyo, New York, Los Angeles, Sydney)
3. Guarda cada respuesta como JSON en `data/raw/api/`
4. Si existe CSV, lo copia a `data/raw/csv/`
5. Registra todo en logs

---

### **STAGE 2: TRANSFORMATION** (Limpieza)

Airflow ejecuta:
```python
python3 scripts/run_pipeline.py  # Función: run_transformation_stage()
```

**Logs esperados**:
```
[2025-12-22 14:00:20] INFO - ===============================================
[2025-12-22 14:00:20] INFO - STAGE 2: TRANSFORMATION
[2025-12-22 14:00:20] INFO - ===============================================
[2025-12-22 14:00:21] INFO - [2.1] Loading raw data...
[2025-12-22 14:00:22] INFO - Loaded 5 JSON files from API
[2025-12-22 14:00:23] INFO - [2.2] Normalizing and cleaning data...
[2025-12-22 14:00:24] INFO - ✓ Removed 0 duplicate records
[2025-12-22 14:00:25] INFO - ✓ Handled missing values
[2025-12-22 14:00:26] INFO - ✓ Standardized datetime formats
[2025-12-22 14:00:27] INFO - [2.3] Saving cleaned data...
[2025-12-22 14:00:28] INFO - ✓ Saved: /data/clean/2025-12-22_merged_clean.parquet
```

**¿Qué sucede?**:
1. Lee JSONs del API desde `data/raw/api/`
2. Lee CSV si existe desde `data/raw/csv/`
3. Normaliza formatos de fecha/hora
4. Valida datos numéricos (temperatura, humedad, etc.)
5. Elimina duplicados
6. Guarda como Parquet en `data/clean/`

---

### **STAGE 3: ANALYTICS** (Agregados)

Airflow ejecuta:
```python
python3 scripts/run_pipeline.py  # Función: run_analytics_stage()
```

**Logs esperados**:
```
[2025-12-22 14:00:30] INFO - ===============================================
[2025-12-22 14:00:30] INFO - STAGE 3: ANALYTICS
[2025-12-22 14:00:30] INFO - ===============================================
[2025-12-22 14:00:31] INFO - [3.1] Loading clean data...
[2025-12-22 14:00:32] INFO - Loaded 150 records
[2025-12-22 14:00:33] INFO - [3.2] Creating analytics views...
[2025-12-22 14:00:34] INFO - ✓ Created VIEW: temperature_stats
[2025-12-22 14:00:35] INFO - ✓ Created VIEW: city_weather_summary
[2025-12-22 14:00:36] INFO - ✓ Created VIEW: daily_aggregates
[2025-12-22 14:00:37] INFO - [3.3] Generating report...
[2025-12-22 14:00:38] INFO - ✓ Saved: /outputs/analytics_report.json
```

**¿Qué sucede?**:
1. Lee datos limpios desde `data/clean/`
2. Crea base de datos DuckDB en `data/analytics/analytics.db`
3. Crea 3 vistas SQL agregadas:
   - `temperature_stats`: Promedio, máximo, mínimo por ciudad
   - `city_weather_summary`: Resumen general por ciudad
   - `daily_aggregates`: Totales diarios
4. Ejecuta queries de análisis
5. Genera reporte JSON en `outputs/analytics_report.json`

---

### **STAGE 4: HEALTH CHECK**

Airflow ejecuta:
```bash
test -f outputs/analytics_report.json && echo "✓ Pipeline successful"
```

**Logs esperados**:
```
[2025-12-22 14:00:40] INFO - ===============================================
[2025-12-22 14:00:40] INFO - HEALTH CHECK
[2025-12-22 14:00:40] INFO - ===============================================
[2025-12-22 14:00:41] INFO - ✓ Analytics report found
[2025-12-22 14:00:42] INFO - ✓ Pipeline execution successful
```

---

## 📊 Ver Logs en Airflow Web UI

### **En el navegador (http://localhost:8081)**:

1. **Ir a DAGs** → `data_lakehouse_pipeline`
2. **Ver gráfico** → Visualiza las 4 tareas
3. **Ir a "Grid"** → Ve todas las ejecuciones
4. **Clickear una ejecución** → Ve detalles
5. **Clickear una tarea** → **Log** → Lee logs completos

### **En la terminal** (dentro del container):

```bash
docker exec data-lakehouse-airflow bash -c \
  "tail -100f /airflow/logs/data_lakehouse_pipeline/*/latest/log"
```

---

## 🔧 Ejecución Manual del Pipeline

Si quieres ejecutar ahora sin esperar:

```bash
# Opción 1: Via Airflow CLI
docker exec data-lakehouse-airflow airflow dags trigger data_lakehouse_pipeline

# Opción 2: Via UI
# 1. Ve a http://localhost:8081
# 2. En "DAGs", busca data_lakehouse_pipeline
# 3. Clickea el botón de play (▶)
```

---

## 📈 Próxima Ejecución

- **data_lakehouse_pipeline**: Mañana a las 2:00 AM UTC
- **data_generation_pipeline**: Este domingo a medianoche UTC

Puedes ver las próximas ejecuciones en la columna "Next Run" en la Web UI.

---

## 🎯 Resumen de Flujo de Datos

```
OpenWeather API        CSV (opcional)
       ↓                    ↓
  [INGESTION]       ----- Extrae datos crudos
       ↓
  /data/raw/
       ↓
  [TRANSFORMATION]   ----- Limpia y normaliza
       ↓
  /data/clean/
       ↓
  [ANALYTICS]        ----- Crea agregados
       ↓
  /data/analytics/
  + /outputs/
       ↓
  📊 analytics_report.json  ----- Resultado final
```

---

## ❓ Preguntas Frecuentes

**P: ¿Dónde veo si falló algo?**
- R: Web UI → DAG → Tarea roja → Log

**P: ¿Cómo evito que se ejecute automáticamente?**
- R: En la UI, pausa el DAG (toggle ON/OFF)

**P: ¿Cómo cambio el horario?**
- R: Edita `dags/main_pipeline_dag.py` → `schedule_interval`

**P: ¿Se sobrescribe la data cada día?**
- R: Sí, cada día sobrescribe `data/clean/` y `outputs/` con datos nuevos

---

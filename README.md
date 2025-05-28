
# 🌦️ ETL Weather Data Pipeline with Apache Airflow & PostgreSQL

This project sets up a simple ETL pipeline using [Apache Airflow](https://airflow.apache.org/) to extract current weather data from the [Open-Meteo API](https://open-meteo.com/), transform it, and load it into a PostgreSQL database.

---

## 📦 Project Structure

```
.
├── dags/
│   └── ETL_weather.py         # Main DAG definition
├── docker-compose.yml         # PostgreSQL service setup
└── README.md                  # Project documentation (this file)
```

---

## 🚀 Features

- **Apache Airflow**: Manages the workflow and tasks.
- **PostgreSQL**: Stores structured weather data.
- **Open-Meteo API**: Source of real-time weather data.
- **ETL Workflow**:
  - **Extract**: Calls Open-Meteo API.
  - **Transform**: Parses required fields.
  - **Load**: Inserts data into PostgreSQL.

---

## 🐳 Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Apache Airflow installed (`astro dev` or via custom setup)

---

## 🔧 Setup

### 1. Clone the repository

```bash
git clone https://github.com/thisisAranya/weather_airflow_project.git
cd weather_airflow_project
```

### 2. Start PostgreSQL via Docker Compose

```bash
docker-compose up -d
```

This starts a PostgreSQL container on port `5432` with:

- **Username**: `postgres`
- **Password**: `postgres`
- **Database**: `postgres`

### 3. Start Airflow

If you're using the Astro CLI:

```bash
astro dev start
```

Or with your custom Airflow setup:

```bash
docker-compose up airflow-webserver airflow-scheduler
```

---

## 🔌 Airflow Connection Setup

### Create two connections from the Airflow UI:

#### 1. PostgreSQL Connection

- **Conn Id**: `postgres_default`
- **Conn Type**: `Postgres`
- **Host**: `postgres` (Docker service name)
- **Login**: `postgres`
- **Password**: `postgres`
- **Schema**: `postgres`
- **Port**: `5432`

> ⚠️ Don't set `database` or `dbname` in Extra field to avoid errors.

#### 2. Open Meteo API Connection

- **Conn Id**: `open_meteo_api`
- **Conn Type**: `HTTP`
- **Host**: `https://api.open-meteo.com`

---

## 📅 DAG Details

- **DAG ID**: `ETL_weather`
- **Schedule**: `@daily`
- **Tasks**:
  - `extract_weather_data`
  - `transform_weather_data`
  - `load_weather_data`

---

## 🗃️ Database Table Schema

```sql
CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    wind_direction FLOAT NOT NULL,
    weather_code INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ✅ Example Output

After a successful run, the `weather` table in PostgreSQL will look like:

| id | latitude | longitude | temperature | wind_speed | wind_direction | weather_code | timestamp |
|----|----------|-----------|-------------|------------|----------------|--------------|-----------|
| 1  | 40.7128  | -74.0060  | 23.5        | 5.1        | 230            | 3            | 2025-05-28 00:00:00 |

---

## 🧪 Testing the DAG

You can trigger the DAG manually:

1. Go to the Airflow UI
2. Find the DAG `ETL_weather`
3. Click **Trigger DAG**

---

## 🧼 Cleanup

To stop services:

```bash
docker-compose down
```

---

## 📝 Author

- [Aranya Saha](https://github.com/thisisAranya)

---

## Acknowledgement
This project has been implemented from a youtube video of Krish Naik.

---

## 📄 License

This project is licensed under the MIT License.

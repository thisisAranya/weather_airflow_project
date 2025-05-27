from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from pendulum import datetime  # ✅ Correct use of pendulum

LATITUDE = 40.7128
LONGITUDE = -74.0060

POST_GRES_CONN_ID = "postgres_default"
API_CONN_ID = "open_meteo_api"

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 5, 1, tz="UTC")
}

with DAG(
    dag_id='ETL_weather',
    default_args=default_args,
    schedule='@daily',  # ✅ Correct for Airflow 2.9+
    catchup=False,
    tags=["example"]
) as dag:

    @task()
    def extract_weather_data():
        """Extracts weather data from an open_meteo_api using HttpHook."""
        http_hook = HttpHook(method='GET', http_conn_id=API_CONN_ID)
        endpoint = f"/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"
        response = http_hook.run(endpoint)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch weather data: {response.status_code} - {response.text}")

        return response.json()

    @task()
    def transform_weather_data(weather_data):
        """Transforms the raw weather data into a structured format."""
        current_weather = weather_data.get("current_weather")

        if not current_weather:
            raise ValueError("No current weather data found in the response.")
        
        return {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "temperature": current_weather["temperature"],
            "wind_speed": current_weather["windspeed"],
            "wind_direction": current_weather["winddirection"],
            "weather_code": current_weather["weathercode"],
        }

    @task()
    def load_weather_data(transformed_data):
        """Loads the transformed weather data into a PostgreSQL database."""
        pg_hook = PostgresHook(postgres_conn_id=POST_GRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
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
        """)

        # Insert the data
        cursor.execute("""
            INSERT INTO weather (latitude, longitude, temperature, wind_speed, wind_direction, weather_code)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            transformed_data["latitude"],
            transformed_data["longitude"],
            transformed_data["temperature"],
            transformed_data["wind_speed"],
            transformed_data["wind_direction"],
            transformed_data["weather_code"]
        ))

        conn.commit()
        cursor.close()
        conn.close()  # ✅ Always close connections

    # DAG pipeline
    raw_data = extract_weather_data()
    processed_data = transform_weather_data(raw_data)
    load_weather_data(processed_data)
Daily Revenue Pipeline
Run
docker compose up -d

Airflow
http://localhost:8080

DAG
daily_revenue_pipeline

Flow
Load yesterday orders
Upsert into staging table
dbt run
dbt test
Tests
unique
not_null
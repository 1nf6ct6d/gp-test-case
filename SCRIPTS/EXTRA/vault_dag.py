from datetime import datetime
from pathlib import Path
from airflow import DAG
from airflow.operators.bash import BashOperator


BASE_DIR = Path(__file__).resolve().parents[2]
API_TO_STG_SCRIPT = BASE_DIR / "SCRIPTS" / "ETL" / "api_to_stg.py"
STG_TO_DDS_SCRIPT = BASE_DIR / "SCRIPTS" / "ETL" / "stg_to_dds.py"

with DAG(
    dag_id="data_vault_auto",
    description="Оркестрация пайплайна. Решил добавить.",
    start_date=datetime(2026, 5, 19),
    schedule=None,
    catchup=False,
    tags=["gazprom_testik", "data_vault"],
) as dag:

    api_to_stg = BashOperator(
        task_id="api_to_stg",
        bash_command=f"python3 {API_TO_STG_SCRIPT}",
    )

    stg_to_dds = BashOperator(
        task_id="stg_to_dds",
        bash_command=f"python3 {STG_TO_DDS_SCRIPT}",
    )

    api_to_stg >> stg_to_dds
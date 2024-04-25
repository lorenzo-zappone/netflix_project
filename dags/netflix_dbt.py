from airflow.decorators import dag, task
from pendulum import datetime
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook, DbtCloudJobRunStatus
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor 

DBT_CLOUD_CONN_ID= "dbt_conn"
JOB_ID = "70403103919838"


@dag(
start_date=datetime(2024,4,18),
schedule="@daily",
catchup=False,
)

def running_dbt_cloud():
    """
    Test running a dbt Cloud job
    """
    dbt_cloud_run_job = DbtCloudRunJobOperator(
        task_id="dbt_cloud_run_job",
        job_id=JOB_ID,
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        check_interval=60,
        timeout=360,
    )

running_dbt_cloud()
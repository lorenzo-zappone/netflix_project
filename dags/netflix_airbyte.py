from airflow.decorators import dag, task
from pendulum import datetime
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook, DbtCloudJobRunStatus
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor 

AIRBYTE_CONN_ID= "airbyte_conn"
AIRBYTE_JOB = "689722eb-2ad7-4f6b-b04b-d8920b490058"

@dag(
start_date=datetime(2024,4,18),
schedule="@daily",
catchup=False,
)

def running_airbyte_job():
    """
    Test running an Airbyte job
    """
    airbyte_netflix_job = AirbyteTriggerSyncOperator(
        task_id="airbyte_trigger_sync",
        airbyte_conn_id=AIRBYTE_CONN_ID,
        connection_id=AIRBYTE_JOB,
        asynchronous=True,
        timeout=360
    )
    airbyte_sensor = AirbyteJobSensor(
        task_id='airbyte_sensor_money_json_example',
        airbyte_conn_id='airbyte_conn_example',
        airbyte_job_id=airbyte_netflix_job.output
    )

running_airbyte_job()
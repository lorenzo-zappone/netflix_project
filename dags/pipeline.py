from airflow.decorators import dag, task
from pendulum import datetime
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook, DbtCloudJobRunStatus
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.providers.dbt.cloud.sensors.dbt import DbtCloudJobRunSensor
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor 

AIRBYTE_CONN_ID= "airbyte_conn"
AIRBYTE_JOB = "689722eb-2ad7-4f6b-b04b-d8920b490058"
DBT_CLOUD_CONN_ID= "dbt_conn"
JOB_ID = "70403103919838"

@dag(
start_date=datetime(2024,4,23),
schedule="@daily",
catchup=False,
)

def running_airbyte_dbt_job():
    """
    Test running an Airbyte and DBT job
    """
    
    airbyte_netflix_job = AirbyteTriggerSyncOperator(
        task_id="airbyte_trigger_sync",
        airbyte_conn_id=AIRBYTE_CONN_ID,
        connection_id=AIRBYTE_JOB,
        asynchronous=True,
        timeout=360
    )
    airbyte_sensor = AirbyteJobSensor(
        task_id='airbyte_sensor_netflix_job',
        airbyte_conn_id=AIRBYTE_CONN_ID,
        airbyte_job_id=airbyte_netflix_job.output
    )
    
    dbt_cloud_run_job = DbtCloudRunJobOperator(
        task_id="dbt_cloud_run_job",
        job_id=JOB_ID,
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        check_interval=60,
        timeout=360,
    )
    
    dbt_cloud_sensor = DbtCloudJobRunSensor(
        task_id='dbt_cloud_sensor_job',
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        run_id=dbt_cloud_run_job.output
    )
    
    airbyte_netflix_job >> airbyte_sensor >> dbt_cloud_run_job >> dbt_cloud_sensor

running_airbyte_dbt_job()
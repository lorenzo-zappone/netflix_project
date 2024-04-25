Running an Airbyte and DBT job with Airflow
This pipeline demonstrates how to run an Airbyte job to sync data from a source, and then run a DBT job to transform and load the data into a destination. The Airflow sensors ensure that the Airbyte job completes successfully before running the DBT job, and that the DBT job completes successfully before the pipeline finishes.

Requirements
To run this pipeline, you need:

An Airflow environment with the necessary Airflow providers installed (e.g. pip install 'apache-airflow[amazon,azure,google,mysql,postgres,ssh,databricks,docker,kubernetes,celery,hashicorp,http,celery,redis,grpc,elasticsearch,spark,statsd,prometheus,kubernetes_executor,kubernetes_pod_operator,kubernetes_secret,postgres,ssh,ssh_hook,ssh_tunnel,http,minio]')
An Airbyte account and an Airbyte source and destination configured
A DBT Cloud account and a DBT project with at least one model configured


Setup
Configure the Airflow environment
1.
Open the Airflow UI in your web browser.
2.
Click on the "Admin" menu item in the top-left corner, then select "Connections" from the dropdown menu.
3.
Click on the "Add" button to create a new connection.
4.
Choose an appropriate connection type (e.g. "SSH") and fill in the necessary information (e.g. hostname, port, username, password, etc.).
5.
Repeat steps 3 and 4 for any additional connections that you need (e.g. an Airbyte connection, a DBT Cloud connection, etc.).


Configure the Airbyte connection
1.
Open the Airbyte UI in your web browser.
2.
Click on the "Settings" icon in the top-right corner, then select "Connections" from the dropdown menu.
3.
Click on the "Add connection" button to create a new connection.
4.
Choose an appropriate source or destination, then fill in the necessary information (e.g. server URL, API key, etc.).
5.
Repeat steps 3 and 4 for any additional connections that you need.


Configure the DBT Cloud connection
1.
Open the DBT Cloud UI in your web browser.
2.
Click on the "Settings" icon in the top-right corner, then select "Connections" from the dropdown menu.
3.
Click on the "Add connection" button to create a new connection.
4.
Choose "dbt Cloud" as the connection type, then fill in the necessary information (e.g. API key, etc.).
5.
Repeat steps 3 and 4 for any additional connections that you need.


Create the DAG file
1.
Create a new Python file (e.g. airflow_pipeline.py) and add the following code to it:

from airflow.decorators import dag, task
from pendulum import datetime
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook, DbtCloudJobRunStatus
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.providers.dbt.cloud.sensors.dbt import DbtCloudJobRunSensor
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor 

# Define the necessary connection IDs
AIRBYTE_CONN_ID = "your_airbyte_conn_id"
DBT_CLOUD_CONN_ID = "your_dbt_cloud_conn_id"

# Define the necessary job IDs
AIRBYTE_JOB = "your_airbyte_job_id"
DBT_CLOUD_JOB = "your_dbt_cloud_job_id"

@dag(
    start_date=datetime(2024, 4, 23),
    schedule="@daily",
    catchup=False,
)
def running_airbyte_dbt_job():
    """
    Test running an Airbyte and DBT job
    """

    # Define the Airbyte task
    airbyte_task = AirbyteTriggerSyncOperator(
        task_id="airbyte_task",
        airbyte_conn_id=AIRBYTE_CONN_ID,
        connection_id=AIRBYTE_JOB,
        asynchronous=True,
        timeout=360,
    )

    # Define the Airbyte sensor
    airbyte_sensor = AirbyteJobSensor(
        task_id="airbyte_sensor",
        airbyte_conn_id=AIRBYTE_CONN_ID,
        airbyte_job_id=airbyte_task.output,
    )

    # Define the DBT Cloud task
    dbt_cloud_task = DbtCloudRunJobOperator(
        task_id="dbt_cloud_task",
        job_id=DBT_CLOUD_JOB,
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        check_interval=60,
        timeout=360,
    )

    # Define the DBT Cloud sensor
    dbt_cloud_sensor = DbtCloudJobRunSensor(
        task_id="dbt_cloud_sensor",
        dbt_cloud_conn_id=DBT_CLOUD_CONN_ID,
        run_id=dbt_cloud_task.output,
    )

    # Define the dependency graph
    airbyte_task >> airbyte_sensor >> dbt_cloud_task >> dbt_cloud_sensor

# Execute the DAG
running_airbyte_dbt_job()

2.
Replace the placeholders with the actual connection IDs and job IDs that you obtained from the previous steps.
3.
Save the file.


Test the pipeline
1.
Open the Airflow UI in your web browser.
2.
Click on the "DAGs" menu item in the top-left corner, then select "Tree" from the dropdown menu.
3.
Find the "running_airbyte_dbt_job" DAG in the tree view, then click on the "Play" button to run the pipeline.
4.
Monitor the pipeline execution status in the "Task Instance" tab.
5.
Once the pipeline has completed successfully, you should be able to see the results in the DBT Cloud UI.

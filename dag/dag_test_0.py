from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'jake',
    # 'depends_on_past': True,
    'start_date': datetime(2016, 8, 30, 10, 15),
    # 'email': ['foo@bar.com'],
    # 'email_on_failure': True,
    # 'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG('etl_dag',\
    default_args=default_args,\
    schedule_interval='15 * * * *')

# Extract task
extract_template = BASE_TASK_PATH +\
    'extract.sh {{ts_nodash}} {{params.user_host}} '+\
    '{{params.remote_dir}} {{params.local_dir}}'
extract_task = BashOperator(
    task_id='extract',
    bash_command=extract_template,
    params={
        'user_host': REMOTE_USER_HOST,
        'remote_dir': REMOTE_PATH,
        'local_dir': DATASET_PATH_ORIG},
    dag=dag)

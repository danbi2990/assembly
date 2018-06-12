if __name__ == "__main__" and __package__ is None:
    import os
    import sys
    cur_dir = os.path.split(os.getcwd())[0]
    if cur_dir not in sys.path:
        sys.path.append(cur_dir)

from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from dag.common import PYTHON, ASSEMBLY

default_args = {
    'owner': 'jake',
    # 'depends_on_past': True,
    'start_date': datetime(2018, 6, 12, 10, 15),
    # 'email': ['foo@bar.com'],
    # 'email_on_failure': True,
    # 'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG('watch_committee_step0',
          default_args=default_args,
          schedule_interval='15 * * * *')

# Extract task
# extract_template = BASE_TASK_PATH +\
#     'extract.sh {{ts_nodash}} {{params.user_host}} '+\
#     '{{params.remote_dir}} {{params.local_dir}}'
task = f'{PYTHON} {ASSEMBLY}/scrape/watch_committee_step0.py'
extract_task = BashOperator(
    task_id='extract',
    bash_command=task,
    # params={
    #     'user_host': REMOTE_USER_HOST,
    #     'remote_dir': REMOTE_PATH,
    #     'local_dir': DATASET_PATH_ORIG},
    dag=dag)

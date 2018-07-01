from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

ASSEMBLY_PYTHON = '$HOME/.virtualenvs/assembly/bin/python3.6'
ASSEMBLY_PROJECT = '$HOME/Dev/assembly'

default_args = {
    'start_date': datetime(2018, 6, 28),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email': [],
    'email_on_failure': True,
    'email_on_retry': False,
}

dag = DAG(
    'assembly_scrape_a_watch_committee',
    default_args=default_args,
)

cmd0 = f'{ASSEMBLY_PYTHON} {ASSEMBLY_PROJECT}/scrape/a0_watch_committee.py'

task0 = BashOperator(task_id='a0_watch_committee',
                     bash_command=cmd0, dag=dag)

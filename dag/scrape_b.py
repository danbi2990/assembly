from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'start_date': datetime(2018, 7, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email': [],
    'email_on_failure': True,
    'email_on_retry': False,
}

dag = DAG(
    'assembly_scrape_a',
    default_args=default_args,
)

cmd0 = 'touch /home/jake/test.txt'

task0 = BashOperator(task_id='b0_touch_file',
                     bash_command=cmd0, dag=dag)

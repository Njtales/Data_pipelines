from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'stock_data_pipeline',
    default_args=default_args,
    description='Pipeline to download and process stock data from Yahoo Finance',
    schedule_interval='0 6 * * *',
)

def download_data():
    # Your code to download stock data from Yahoo Finance goes here
    pass

def process_data():
    # Your code to process the downloaded data goes here
    pass

def load_data():
    # Your code to load the processed data into a data warehouse goes here
    pass

download_data_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data,
    dag=dag,
)

process_data_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag,
)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

download_notification_task = EmailOperator(
        task_id='download_notification',
        to='youremail@example.com',
        subject='Stock Data Pipeline: Download Complete',
        html_content='<p>The download step in the stock data pipeline has completed successfully.</p>',
        dag=dag
)

process_notification_task = EmailOperator(
        task_id='process_notification',
        to='youremail@example.com',
        subject='Stock Data Pipeline: Process Complete',
        html_content='<p>The process step in the stock data pipeline has completed successfully.</p>',
        dag=dag
)

load_notification_task = EmailOperator(
        task_id='load_notification',
        to='youremail@example.com',
        subject='Stock Data Pipeline: Load Complete',
        html_content='<p>The load step in the stock data pipeline has completed successfully.</p>',
        dag=dag
)

download_data_task >> download_notification_task >> process_data_task >> process_notification_task >> load_data_task >> load_notification_task
# Import required libraries and modules
from datetime import datetime, timedelta
import pytz
from airflow import DAG
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

# Define the default arguments for the DAG
default_args = {
    'owner': 'me',  # the owner of the DAG
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 2, tzinfo=pytz.utc),  # the start date of the DAG
    'email_on_failure': True,  # send an email if a task fails
    'email_on_retry': False,
    'retries': 3,  # the number of times to retry a failed task
    'retry_delay': timedelta(minutes=0.05),  # the amount of time to wait before retrying a failed task
    'concurrency': 1,  # the maximum number of tasks to run simultaneously
    'schedule_interval': '0 7 * * *', # set the schedule interval to run daily at 7 am BST
    'timezone': 'Europe/London' # set the timezone to Europe/London
}

# Create the DAG object
dag = DAG(
    dag_id='SP500_Stock_data_pipeline',  # the ID of the DAG
    default_args=default_args,
    description='Pipeline to download and process stock data from Yahoo Finance',
    # schedule_interval='0 6 * * *',  # the interval at which the DAG should run
)

# Define the download_data() function
def download_data():
    # Define the date range for which to download data
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.Timedelta(days=365)

    # Define the list of companies in the S&P 500 index
    sp500_companies = ['AAPL', 'MSFT', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'BRK.B', 'V', 'PG', 'XOM', 'CSCO', 'ACN', 'CVX', 'NKE', 'WMT', 'BLK', 'ADP', 'CME', 'CL', 'NVDA', 'JPM', 'UNH', 'HD', 'BAC', 'MA', 'ADBE', 'CRM', 'PFE', 'CMCSA', 'PYPL', 'PEP', 'ABT', 'COST', 'KO', 'MRK', 'LLY', 'INTC', 'QCOM', 'LIN', 'TXN','NEE','INTU','MDT','UNP','HON','UPS','PM','AMAT','RTX','NOW','BMY','TGT','SCHW','AMGN','CAT','PLD']

    # Download stock data for each company
    stock_data = {}

    for company in sp500_companies:
        try:
            stock_data[company] = yf.download(
                tickers=company,
                start=start_date,
                end=end_date
            )
        except Exception as e:
            print(f"Failed to get data for {company}. Error: {str(e)}")

    # Concatenate the data into a single DataFrame
    stock_data = pd.concat(stock_data.values(), keys=stock_data.keys())

    # Save the data to a CSV file
    stock_data.to_csv('/opt/airflow/datasets/SP500_data/SP500_Stock_data.csv')

# Define the process_data() function
# Define the function to process the stock data
def process_data():
    # Load the data from the CSV file
    stock_data = pd.read_csv("/opt/airflow/datasets/SP500_data/SP500_Stock_data.csv", index_col=[0, 1], parse_dates=[1])

    # Clean the data by removing any rows with missing values
    stock_data = stock_data.dropna()

    # Remove any duplicate rows
    stock_data = stock_data.drop_duplicates()

    # Calculate additional metrics
    stock_data['daily_return'] = stock_data.groupby(level=0)['Adj Close'].pct_change()
    stock_data['moving_average_5'] = stock_data.groupby(level=0)['Adj Close'].rolling(5).mean().droplevel(0)
    stock_data['moving_average_20'] = stock_data.groupby(level=0)['Adj Close'].rolling(20).mean().droplevel(0)

    # Save the processed data to a new CSV file
    stock_data.to_csv('/opt/airflow/datasets/SP500_data/processed_SP500Stock_data.csv')

# Define the function to load the processed data into a database
def load_data():
    # Create a database engine
    engine = create_engine('postgresql://airflow:airflow@172.19.0.3/airflow')

    # Load the processed data from the CSV file
    stock_data = pd.read_csv('/opt/airflow/datasets/SP500_data/processed_SP500Stock_data.csv', index_col=[0, 1], parse_dates=[1])

    # Load the data into a table in the data warehouse
    stock_data.to_sql('SP500Stock_data', engine, if_exists='replace')

# Define the function to send email notifications when the pipeline completes
def send_notifications():
    # Define the email parameters
    to = 'youremail@example.com'
    subject = 'Stock Data Pipeline: Completed Successfully'
    html_content = '<p>The stock data pipeline has completed successfully.</p>'

    # Send the email
    send_email(to, subject, html_content)

# Download data task
download_data_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data,
    dag=dag,
)

# Send notification after download task completes
download_notification_task = EmailOperator(
        task_id='download_notification',
        to='youremail@example.com',
        subject='Stock Data Pipeline: Download Complete',
        html_content='<p>The download step in the stock data pipeline has completed successfully.</p>',
        dag=dag
)

# Process data task
process_data_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag,
)

# Send notification after process task completes
process_notification_task = EmailOperator(
        task_id='process_notification',
        to='youremail@example.com',
        subject='Stock Data Pipeline: Process Complete',
        html_content='<p>The process step in the stock data pipeline has completed successfully.</p>',
        dag=dag
)

# Load data task
load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

# Send notification after load task completes
load_notification_task = EmailOperator(
        task_id='load_notification',
        to='youremail@example.com',
        subject='Stock Data Pipeline: Load Complete',
        html_content='<p>The load step in the stock data pipeline has completed successfully.</p>',
        dag=dag
)

# Send notification after all tasks complete
send_notifications_task = PythonOperator(
    task_id='send_notifications',
    python_callable=send_notifications,
    dag=dag,
)

# Define the task dependencies
download_data_task >> download_notification_task >> process_data_task >> \
process_notification_task >> load_data_task >> load_notification_task >> send_notifications_task

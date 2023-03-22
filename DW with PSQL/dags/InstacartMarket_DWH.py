from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
from zipfile import ZipFile

# IN PROGRESS

default_args = {
    'owner': 'me',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 7),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=0.05),
    # 'concurrency': 1
}

dag = DAG(
    dag_id = 'Instacart_Market_Data_to_DWH_postgres',
    default_args=default_args,
    description='A data pipeline that downloads the data from kaggle dataset link,\
    extracts Instacart Market Data from a CSV file, performs some basic transformations,\
    create tables for each csv file and loads it into a Usr_Pokemon table in PostgreSQL database.',
    schedule_interval=None
)

# Task 1: Extract data from CSV file
def extract_data():

    # Extract the CSV file from zip
    # zf = ZipFile('/opt/airflow/datasets/instacart_market_basket/archive.zip', 'r')
    # zf.extractall('/opt/airflow/datasets/instacart_market_basket')
    # zf.close()
    pass


task_extract_Data = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

# Task 2: Transform data
def create_tables():
    conn = psycopg2.connect(database = 'instacart_market', 
                            user = 'airflow',
                            password='airflow',
                            host='172.23.0.3',
                            port='5432')
    cursor = conn.cursor()
    cursor.execute("""
    
DROP TABLE IF EXISTS aisles;
CREATE TABLE aisles (
    aisle_id INTEGER PRIMARY KEY,
    aisle VARCHAR(255)
    );

DROP TABLE IF EXISTS products;
CREATE TABLE products (
	product_id INTEGER PRIMARY KEY,
	product_name VARCHAR(255),
	aisle_id INTEGER,
	department_id INTEGER
    );

DROP TABLE IF EXISTS order_products__train;
CREATE TABLE order_products__train (
	product_id INTEGER PRIMARY KEY,
	order_id INTEGER,
	add_cart_order INTEGER,
	reordered INTEGER
    );

DROP TABLE IF EXISTS order_products__prior;
CREATE TABLE order_products__prior (
	product_id INTEGER PRIMARY KEY,
	order_id INTEGER,
	add_cart_order INTEGER,
	reordered INTEGER
    );

DROP TABLE IF EXISTS departments;
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department VARCHAR(255)
    );

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    eval_set VARCHAR(255),
    order_number INTEGER,
    order_dow INTEGER,
    order_hour_of_day INTEGER,
    days_since_prior_order INTEGER
    );
    
    """)


task_create_tables= PythonOperator(
    task_id='create_tables',
    python_callable=create_tables,
    dag=dag,
)

# Task 3: Load data into PostgreSQL database
def load_data():
    conn = psycopg2.connect(database = 'instacart_market', 
                            user = 'airflow',
                            password='airflow',
                            host='172.23.0.3',
                            port='5432')
    cursor = conn.cursor()

    with open('/opt/airflow/datasets/instacart_market_basket/aisles.csv', 'r') as f:
        next(f) # skip the header row
        cursor.copy_from(f, 'aisles', sep=',')

    with open('/opt/airflow/datasets/instacart_market_basket/products.csv', 'r') as f:
        next(f) # skip the header row
        cursor.copy_from(f, 'products', sep=',')
    
    with open('/opt/airflow/datasets/instacart_market_basket/order_products__train.csv', 'r') as f:
        next(f) # skip the header row
        cursor.copy_from(f, 'order_products__train', sep=',')

    with open('/opt/airflow/datasets/instacart_market_basket/order_products__prior.csv', 'r') as f:
        next(f) # skip the header row
        cursor.copy_from(f, 'order_products__prior', sep=',')

    with open('/opt/airflow/datasets/instacart_market_basket/orders.csv', 'r') as f:
        next(f) # skip the header row
        cursor.copy_from(f, 'orders', sep=',')

    with open('/opt/airflow/datasets/instacart_market_basket/departments.csv', 'r') as f:
        next(f) # skip the header row
        cursor.copy_from(f, 'departments', sep=',')
    
    conn.commit()
    cursor.close()
    conn.close()

task_load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

task_extract_Data >> task_create_tables >> task_load_data

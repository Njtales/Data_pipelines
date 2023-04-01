from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
from zipfile import ZipFile

default_args = {
    'owner': 'me',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=0.05),
    'concurrency': 1
}

dag = DAG(
    dag_id = 'PokemonData_to_PostgresQL',
    default_args=default_args,
    description='A simple data pipeline that extracts Pokemon data from a CSV file, performs some basic transformations, and loads it into a Usr_Pokemon table in PostgreSQL database.',
    schedule_interval=None
)

# Task 1: Extract data from CSV file
def extract_data():

    # Extract the CSV file from zip
    zf = ZipFile('/opt/airflow/datasets/Pokemon_data/archive.zip', 'r')
    zf.extractall('/opt/airflow/datasets/Pokemon_data')
    zf.close()


task_extract_Data = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

# Task 2: Transform data
def transform_data():

    df = pd.read_csv('/opt/airflow/datasets/Pokemon_data/pokemon.csv')
    df['Type 2'] = df['Type 2'].fillna("NA")


    ## column names capitalize
    df.columns = df.columns.str.capitalize()

    df.to_csv('/opt/airflow/datasets/Pokemon_data/transformed_data.csv', index=False)

task_transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

# Task 3: Load data into PostgreSQL database
def load_data():
    conn = psycopg2.connect(database = 'airflow', 
                            user = 'airflow',
                            password='airflow',
                            host='172.21.0.3',
                            port='5432')
    cursor = conn.cursor()

    cursor.execute("""

    DROP TABLE IF EXISTS usr_pokemon;

    CREATE TABLE usr_pokemon (
    ID INTEGER,
    Name TEXT,
    Type_1 TEXT,
    Type_2 TEXT,
    Total INTEGER,
    HP INTEGER,
    Attack INTEGER,
    Defense INTEGER,
    Sp_Atk INTEGER,
    Sp_Def INTEGER,
    Speed INTEGER,
    Generation INTEGER,
    Legendary BOOLEAN
    );
    """)

    with open('/opt/airflow/datasets/Pokemon_data/transformed_data.csv', 'r') as f:
        next(f) # skip the header row
        cursor.copy_from(f, 'usr_pokemon', sep=',')

    conn.commit()
    cursor.close()
    conn.close()

task_load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

task_extract_Data >> task_transform_data >> task_load_data

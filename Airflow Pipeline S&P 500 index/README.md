# Airflow S&P500 Stock Data Pipeline

## Project Description:
The project involves building an Airflow pipeline to download stock data from Yahoo Finance, process it, and load it into a data warehouse. The pipeline will run daily and will download data for all the companies listed in the S&P 500 index.

## Prerequisites

Before running this project, I used the following installed, I reccomend you the same:

- Docker Compose [version v2.15.1 or later]
- PostgreSQL [version 13.10 or later]

## Pipeline Steps:

1. Download Data: Airflow will use a Python script to download stock data for all the companies listed in the S&P 500 index from Yahoo Finance using the pandas-datareader library. The script will output the data as a CSV file.
2. Process Data: Airflow will use another Python script to process the data downloaded in the previous step. The script will clean the data, remove any duplicates, and calculate additional metrics such as daily returns and moving averages.
3. Load Data: Airflow will use a third Python script to load the processed data into a data warehouse. The script will connect to the data warehouse using SQLAlchemy and load the data into a table.
4. Send Notifications: Airflow will send email notifications to the user after each step in the pipeline is completed. If there are any errors or failures in the pipeline, the user will receive an email notification with the details.

## Building and Running the Docker Container

To build and run the Docker container for this project, follow these steps:

1. Clone this repository to your local machine.
2. Open a terminal window and navigate to the root directory of the project.
3. Run the following command to build the Docker container:

>docker-compose build

4. Once the container has finished building, run the following command to start the container:

>docker-compose up

5. The container should now be running. To access the Airflow web interface, open a web browser and go to [http://localhost:8080](http://localhost:8080).

## Connecting to PostgreSQL

This project uses a PostgreSQL database to store [practice data for complex sql and analysis operations]. To connect to the PostgreSQL database, follow these steps:

1. Open pgAdmin4 in your browser at [http://localhost:9090](http://localhost:9090).
2. Enter your credentials mentioned in 'pgAdmin' service mentioned in docker-compose yaml file (change it accordingly). 
3. Use the credentials mentioned in 'postgres' service to connect to desired server in pgAdmin4 and you are good to go.


## Pipeline Schedule:
The pipeline will run daily at 7:00 AM BST. If any step in the pipeline fails, Airflow will retry the step up to three times before sending an email notification to the user.
This project showcases your skills in working with Airflow, Python, data processing, and data warehousing. You can also customize the project by adding more features such as data visualization, error handling, and more.

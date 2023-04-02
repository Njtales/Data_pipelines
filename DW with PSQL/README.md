# Data Warehousing with airflow and PSQL

This project contains simple pipelines created for practice.

## Prerequisites

Before running this project, I used the following installed, I reccomend you the same:

- Docker Compose [version v2.15.1 or later]
- PostgreSQL [version 13.10 or later]

I have downloaded the dataset from [kaggle](https://www.kaggle.com/competitions/instacart-market-basket-analysis/data), and extracted it here (..\DW with apache airflow and PSQL\datasets\instacart_market_basket)

## Building and Running the Docker Container

To build and run the Docker container for this project, follow these steps:

1. Clone this repository to your local machine.
2. Open a terminal window and navigate to the root directory of the project.
3. Run the following command to build the Docker container:

docker-compose build

4. Once the container has finished building, run the following command to start the container:

docker-compose up


5. The container should now be running. To access the Airflow web interface, open a web browser and go to [http://localhost:8080](http://localhost:8080).

## Connecting to PostgreSQL

This project uses a PostgreSQL database to store [practice data for complex sql and analysis operations]. To connect to the PostgreSQL database, follow these steps:

1. Open pgAdmin4 in your browser at [http://localhost:9090](http://localhost:9090).
2. Enter your credentials mentioned in 'pgAdmin' service mentioned in docker-compose yaml file (change it accordingly). 
3. Use the credentials mentioned in 'postgres' service to connect to desired server in pgAdmin4 and you are good to go.

## Troubleshooting

If you experience any issues while running this project, try the following:

- Use this for reference(https://www.linkedin.com/pulse/building-server-postgres-airflow-simple-way-docker-rabelo-saraiva/)

- Try to play around with error
- Still facing issues? Connect to me.

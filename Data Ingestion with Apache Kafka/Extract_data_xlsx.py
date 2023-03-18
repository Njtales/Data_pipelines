import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import datetime

# Set up Alpha Vantage API key
API_KEY = 'CT31LBIPKL4KQX6D'

# Specify the stock symbol to retrieve data for
symbol = 'GOOGL'

# Connect to the Alpha Vantage API and retrieve intraday stock data
ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')

# Extract the close price data and rename the column to the stock symbol
close_data = data['4. close']
close_data.rename(symbol, inplace=True)

# Create a DataFrame with the same index as close_data
df = pd.DataFrame(index=close_data.index)

# Join the close_data with the new DataFrame
df = df.join(close_data)

# Check if a file with today's date minus one day already exists
if os.path.isfile(('E:\Working dir\Data Pipelines\Data Ingestion with Apache Kafka\Data/'\
            + str(datetime.date.today() - datetime.timedelta(days=1)) + '.xlsx')) :
    print("File already exists!")
else:
    # Print the first few rows of the DataFrame and save it to an Excel file
    print(df.head())
    df.to_excel('E:\Working dir\Data Pipelines\Data Ingestion with Apache Kafka\Data/'\
            + str(datetime.date.today() - datetime.timedelta(days=1)) + '.xlsx')

## Project Title
This project aims to import data quickly from Alpha Vantage and analyze the time series data using the Prophet model.

###Getting Started

####Prerequisites

This project requires the following Python packages:

pandas
alpha_vantage
prophet
matplotlib

You can install them using pip:
> pip install pandas alpha_vantage prophet matplotlib

####Usage

1. Import data from Alpha Vantage and save it in a CSV file.
2. Load the CSV file using pandas and convert the date column to datetime format.
3. Rename the columns to 'ds' and 'y'.
4. Create a Prophet model and fit it with the dataset.
5. Create a dataframe with future time periods and make forecasts.
6. Visualize the results using matplotlib.

####Example

Here is a sample code for importing data for GOOGL stock, creating a Prophet model, and making forecasts:

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from prophet import Prophet
import matplotlib.pyplot as plt

# Import data from Alpha Vantage and save it in a CSV file
API_KEY = 'your_api_key_here'
symbol = 'GOOGL'
ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
close_data = data['4. close']
close_data.rename(symbol, inplace=True)
df = pd.DataFrame(index=close_data.index).join(close_data)
df.to_csv('GOOGL.csv')

# Load the CSV file using pandas and convert the date column to datetime format
df = pd.read_csv('GOOGL.csv')
df['ds'] = pd.to_datetime(df['date'])

# Rename the columns to 'ds' and 'y'
df = df.rename(columns={'date': 'ds', 'GOOGL': 'y'})

# Create a Prophet model and fit it with the dataset
model = Prophet()
model.fit(df)

# Create a dataframe with future time periods and make forecasts
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

# Visualize the results using matplotlib
model.plot(forecast)
plt.show()
model.plot_components(forecast)
plt.show()

####Authors
Nikhil
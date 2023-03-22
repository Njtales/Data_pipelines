## Let's import data quickly from Alpha vantage. 

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
API_KEY = 'CT31LBIPKL4KQX6D'
symbol = 'GOOGL'
ts = TimeSeries(key=API_KEY, output_format='pandas')
# data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
data, meta_data = ts.get_daily(symbol='GOOGL', outputsize='full')
close_data = data['4. close']
close_data.rename(symbol, inplace=True)
df = pd.DataFrame(index=close_data.index).join(close_data)
df.to_csv('E:\Working dir\Data_Engg\Time Series Analysis with Prophet\Data/'\
        + symbol + ".csv")

### Now we have a file in dir 'data' containing timestamp and a value.

## Load the dataset

import pandas as pd

### Load the dataset
GOOGL = pd.read_csv('E:\Working dir\Data_Engg\Time Series Analysis with Prophet\data/GOOGL.csv')

### Convert the date column to datetime format
GOOGL['date'] = pd.to_datetime(GOOGL['GOOGL'])

# Rename columns to 'ds' and 'y'
GOOGL = GOOGL.rename(columns={'date': 'ds', 'GOOGL': 'y'})

# df['ds'] = pd.to_datetime(df['ds'])

## Create a Prophet model

from prophet import Prophet

### Create a new Prophet model
model = Prophet()

### Fit the model with the dataset
model.fit(GOOGL)

## Make forecasts
## Create a dataframe with future time periods
future = model.make_future_dataframe(periods=365)

### Make forecasts
forecast = model.predict(future)

## Visualize the results
import matplotlib.pyplot as plt

### Plot the forecast
model.plot(forecast)
plt.show()

# Plot the components of the forecast
model.plot_components(forecast)
plt.show()
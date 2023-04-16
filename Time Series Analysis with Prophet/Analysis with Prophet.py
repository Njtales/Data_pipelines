import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from prophet import Prophet
import matplotlib.pyplot as plt

API_KEY = 'CT31LBIPKL4KQX6D'
symbol = 'GOOGL'
data_dir = './Data/'

# Retrieve data from Alpha Vantage
ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
close_data = data['4. close']
close_data.rename(symbol, inplace=True)

# Save data to CSV
close_data.to_csv(data_dir + symbol + '.csv')

# Load data from CSV
GOOGL = pd.read_csv(data_dir + symbol + '.csv', index_col='date', parse_dates=True)
GOOGL = GOOGL.rename(columns={'4. close': 'y'})

# Create and fit Prophet model
model = Prophet()
model.fit(GOOGL)

# Make forecasts
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

# Visualize results
model.plot(forecast)
plt.show()
model.plot_components(forecast)
plt.show()

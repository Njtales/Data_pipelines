# Import required libraries
from alpha_vantage.timeseries import TimeSeries
from confluent_kafka import Producer

# Set API key and symbol of stock to get data for
API_KEY = 'CT31LBIPKL4KQX6D'
symbol = 'GOOGL'

# Instantiate TimeSeries object and Kafka Producer object
ts = TimeSeries(key=API_KEY, output_format='pandas')  
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Get intraday stock data and convert it to a dictionary
data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
data_dict = data.to_dict()

# Iterate through the dictionary and send each data point to Kafka topic 'alphavantage'
for index, row in data_dict['4. close'].items():
    producer.produce('alphavantage', key=index.strftime('%Y-%m-%d %H:%M:%S').encode('utf-8'), value=str(row).encode('utf-8')), 
    value=str(row).encode('utf-8')

# Flush the Kafka Producer buffer to ensure all messages are sent
producer.flush()

# The following code can be used to verify that messages were sent to the Kafka topic
# for index, row in data['4. close'].iteritems():
#     key = index.strftime('%Y-%m-%d %H:%M:%S').encode()
#     value = str(row).encode()
#     try:
#         producer.send('alphavantage', key=key, value=value)
#         print(f"Sent message: {key} - {value}")
#     except Exception as e:
#         print(f"Error sending message: {e}")
# producer.flush()

# Import required libraries
from alpha_vantage.timeseries import TimeSeries
from kafka import KafkaProducer, KafkaConsumer
from pymongo import MongoClient

# API key for Alpha Vantage API
API_KEY = 'CT31LBIPKL4KQX6D'

# Stock symbol
symbol = 'GOOGL'

# Initializing Alpha Vantage API
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Fetching intraday stock data for the given symbol
data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')

# Initializing Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Sending each data point to Kafka topic 'alphavantage'
for index, row in data['4. close'].iteritems():
    producer.send('alphavantage', key=index.strftime('%Y-%m-%d %H:%M:%S').encode(), value=str(row).encode())

# Ensuring all messages are sent before moving ahead
producer.flush()

# Initializing Kafka consumer
consumer = KafkaConsumer('alphavantage', bootstrap_servers=['localhost:9092'])

# Initializing MongoDB client and database
client = MongoClient('mongodb://localhost:27017')
db = client['Stock_data_Alphavantage']

# Creating collection for the given stock symbol
collection = db[symbol]

# Starting the consumer
print("Consumer started")
for message in consumer:
    try:
        # Decoding the key and value of the received message
        key = message.key.decode()
        value = message.value.decode()

        # Checking if a data point with the same timestamp already exists in the MongoDB collection
        if collection.find_one({'timestamp': key}) is not None:
            print(f"Skipping duplicate data point with timestamp {key}")
            continue

        # Inserting the received data point into MongoDB
        collection.insert_one({'timestamp': key, 'price': value})

        # Printing the key-value pair for confirmation
        print("Inserted data point with timestamp " + key)
    except Exception as e:
        print(f"Error: {e}")

# Checking on console if consumer received the messages!
# for message in consumer:
#     print(f"Received message: {message.key} - {message.value}")
#     key = message.key.decode()
#     value = message.value.decode()
#     collection.insert_one({'timestamp': key, 'price': value})
from alpha_vantage.timeseries import TimeSeries
from kafka import KafkaProducer, KafkaConsumer
from pymongo import MongoClient

API_KEY = 'CT31LBIPKL4KQX6D'
symbol = 'GOOGL'

ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
for index, row in data['4. close'].iteritems():
    producer.send('alphavantage', key=index.strftime('%Y-%m-%d %H:%M:%S').encode(), value=str(row).encode())
producer.flush()

consumer = KafkaConsumer('alphavantage', bootstrap_servers=['localhost:9092'])
client = MongoClient('mongodb://localhost:27017')
db = client['Stock_data_Alphavantage']
collection = db[symbol]
print("Consumer started")
for message in consumer:
    try:
        key = message.key.decode()
        value = message.value.decode()
        print("key : " + str(key), "value : " + str(value))
        collection.insert_one({'timestamp': key, 'price': value})
    except Exception as e:
        print(f"Error: {e}")


# Checking on console if consumer received the messages!
# for message in consumer:
#     print(f"Received message: {message.key} - {message.value}")
#     key = message.key.decode()
#     value = message.value.decode()
#     collection.insert_one({'timestamp': key, 'price': value})
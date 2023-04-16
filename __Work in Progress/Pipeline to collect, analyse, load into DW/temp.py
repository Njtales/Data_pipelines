import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.amazon.com/s?k=iphone'

# Send a GET request to the specified URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the product names and prices
product_names = []
prices = []

for product in soup.find_all('div', {'class': 's-result-item'}):
    product_name = product.find('h2').text.strip()
    price = product.find('span', {'class': 'a-price-whole'}).text.strip()
    product_names.append(product_name)
    prices.append(price)

# Write the data to a CSV file
with open('E:\Working dir\Data_Engg\Pipeline to collect, analyse, load into DW/amazon_products.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price'])

    for i in range(len(product_names)):
        writer.writerow([product_names[i], prices[i]])

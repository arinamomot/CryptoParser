import requests
import csv

# Define the API endpoint
url = 'https://cvizor.com/api/v2/screener/tables'

# Function to fetch futures coins
def fetch_futures_coins():
    url = 'https://cvizor.com/api/v1/screener/settings'
    response = requests.get(url)
    data = response.json()
    futures_coins = [pair['symbol'] for pair in data['pairs'] if pair['is_futures']]
    return futures_coins

# Fetch the data from the API
response = requests.get(url)
data = response.json()

# Define the intervals we are interested in
intervals = data['intervals']

# Fetch futures coins
coins = fetch_futures_coins()

# Create a dictionary to store the rsi14 values for each coin
rsi14_values = {}

# Parse the data
for coin_data in data['data']:
    for coin in coins:
        if coin_data['coin']['label'] == coin:
            coin_label = coin_data['coin']['label']
            rsi14_values[coin_label] = {}
            for interval in intervals:
                if interval in coin_data:
                    rsi14_values[coin_label][interval] = coin_data[interval]['rsi14']

# Write the data to a CSV file
with open('rsi14_values.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    header = ['Coin'] + intervals
    writer.writerow(header)
    # Write the data
    for coin, rsi_values in rsi14_values.items():
        row = [coin] + [rsi_values.get(interval, '') for interval in intervals]
        writer.writerow(row)

print("Data has been written to rsi14_values.csv")

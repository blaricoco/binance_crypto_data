import csv
from os import write 
from datetime import datetime

#Get historical data of particular symbol
async def historical_data(client, symbol, date):
    name = symbol + "_" + date
    data = await client.get_historical_klines(symbol, client.KLINE_INTERVAL_1HOUR,date)
    await write_data(data, name)
#Get all current prices
async def get_all_prices(client):
    now = datetime.now()
    timestamp = str(datetime.timestamp(now))
    price_list = await client.get_all_tickers()
    for data in price_list:
        await write_dict(data, timestamp)
#Write data to csv
async def write_data(data, name):
    with open(name + '.csv', 'w', newline='') as csvfile:
        datawriter = csv.writer(csvfile)
        datawriter.writerows(data)
#Write dictionary to csv
async def write_dict(data, name):
    with open(name + '.csv', 'a', newline='') as csvfile:
        csvfile.write("%s,%s\n"%(data["symbol"],data["price"]))
    


import binance_config 
import asyncio
import time
from binance import BinanceSocketManager, AsyncClient
from binance_functionality import write_data, historical_data, get_all_prices, write_dict

async def kline_listener(client, symbol):
    bm = BinanceSocketManager(client)
    res_count = 0
    async with bm.kline_socket(symbol=symbol) as stream:
        while True:
            data = await stream.recv()
            write_data(data)
            res_count += 1

            if res_count == 5:
                res_count = 0
                loop.call_soon(asyncio.create_task,get_all_prices(client))


async def main():
    #Client configuration
    client = await AsyncClient.create(api_key=binance_config.api_key,
                                      api_secret=binance_config.api_secret)

    #Get all current prices
    while True:
        await asyncio.create_task( get_all_prices(client))
        time.sleep(5)
    #
    #for symbol in binance_config.symbols:
    #    await asyncio.create_task( historical_data(client, symbol, binance_config.date))

    #Close client   
    await client.close_connection()
    
    


if __name__ == "__main__":
    #Create continuous currning loop
    loop = asyncio.get_event_loop()
    #Run main
    loop.run_until_complete(main())
import asyncio
import pandas as pd
from datetime import datetime
import os
from steam_market_api import SteamMarketAPI
import time
import logging
import boto3
from botocore.exceptions import ClientError

async def main():
    s3 = boto3.client('s3')

    start = 0
    count = 100
    raw_data_list = []
    api = SteamMarketAPI()

    start_time = time.time()

    total_count = await api.get_total_count(0, 1)
    print(total_count)

    while True:
        raw_data = await api.fetch_items(start, count)

        raw_data_list.append(raw_data)

        print(start, "-", count)
        start += 100
        count += 100
        if start >= total_count:
            break

        await asyncio.sleep(15)

    if not os.path.exists("raw_data"):
        os.makedirs("raw_data")

    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df = pd.DataFrame(raw_data_list)
    file_path = f'raw_data/cs2_items_raw_{current_datetime}.json'
    df.to_json(file_path, orient='records', indent=4)

    try:
        response = s3.upload_file(f'raw_data/cs2_items_raw_{current_datetime}.json', 'steam-market-s3', f'raw_data/cs2_items_raw_{current_datetime}.json')

        end_time = time.time()
        print("Execution time:", end_time-start_time, "seconds")
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    asyncio.run(main())
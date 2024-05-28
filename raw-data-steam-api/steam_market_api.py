import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SteamMarketAPI:
    def __init__(self):
        self.base_url = "https://steamcommunity.com/market/search/render/?appid=730&norender=1"

    async def get_total_count(self, start, count):
        url = f"{self.base_url}&start={start}&count={count}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            total_count = data.get("total_count", 0)

            return total_count
        except Exception as e:
            logger.error(f"Error fetching items: {e}")
            return 0, []

    async def fetch_items(self, start, count):
        url = f"{self.base_url}&start={start}&count={count}"
        try:
            raw_data_response = requests.get(url)
            raw_data_response.raise_for_status()
            raw_data = raw_data_response.json()
            raw_data_results = raw_data.get("results", [])

            return raw_data_results
        except Exception as e:
            logger.error(f"Error fetching items: {e}")
            return 0, []
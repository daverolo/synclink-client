import httpx
from loguru import logger


class API:
    def __init__(self, apiUrl):
        self.apiUrl = apiUrl
        self.client = httpx.AsyncClient(base_url=apiUrl)

    async def request(self, url_path):
        try:
            response = await self.client.get(url_path)
            response.raise_for_status()

            return response.json()
        except Exception as exc:
            str_exc = str(exc).strip()
            if str_exc != "":
                logger.debug(f"{str_exc}")
            else:
                logger.debug(f"Unknown exception on {self.apiUrl + url_path}")


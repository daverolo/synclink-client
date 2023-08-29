from core.config import Config
from services.eth2api import ETH2API
from services.synclink_api import SyncLink


class Node():
    def __init__(self, url) -> None:
        self.url = url
        self.api = ETH2API(url)
        self.synclink = SyncLink(url)
        self.config = Config()

    async def is_ready(self) -> bool:
        try:
            r = await self.synclink.server.is_ready()
            r.raise_for_status()

            return True
        except:
            return False

    async def get_config(self) -> bool:
        config = await self.synclink.server.config()
        self.config = config

    async def is_syncing(self) -> bool:
        try:
            r = await self.api.node.syncing()

            return bool(r.data.is_syncing)
        except:
            # Consider node as syncing (= NOT synced) on exceptions.
            # This is likely not the best option but ok for the moment.
            return True

import core.synclink
from config.config import config
from loguru import logger


async def startup():
    await core.synclink.client.start()
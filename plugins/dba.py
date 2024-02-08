from aiohttp import ClientSession
from .common import MarketplacePlugin


class Plugin(MarketplacePlugin):
    def __init__(self, session: ClientSession, search_term: str) -> None:
        name = "DBA"
        color = 0x010C8D
        super().__init__(name, color, session, search_term)

    async def fetch_listings(self):
        return print(self.name)

from dataclasses import dataclass
from aiohttp import ClientSession


@dataclass
class MarketplaceListing:
    name: str
    image_url: str
    url: str
    price: str

    def __str__(self) -> str:
        return self.name


class MarketplacePlugin:
    def __init__(
        self, name: str, color: int, session: ClientSession, search_term: str
    ) -> None:
        self.name = name
        self.color = color
        self.session = session
        self.search_term = search_term

    async def fetch_listings(self) -> list[MarketplaceListing]:
        raise NotImplementedError(f"{self.name} plugin must implement `fetch_listings`")

from base64 import b64encode
from dataclasses import dataclass
import json
import aiofiles
from aiofiles import os
from aiohttp import ClientSession
from dataclasses_json import dataclass_json


@dataclass_json
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
        self, name: str, color: int, session: ClientSession, search_url: str
    ) -> None:
        self.name = name
        self.color = color
        self.session = session
        self.search_url = search_url

    async def fetch_listings(self) -> list[MarketplaceListing]:
        """Returns a list of new listings since last run."""
        raise NotImplementedError(f"{self.name} plugin must implement `fetch_listings`")

    async def get_saved_listings(self) -> list[MarketplaceListing]:
        """Returns a list of processed listings."""
        file_name = f"listing_data/{self.name}{self.search_term}.json"
        if await os.path.isfile(file_name):
            async with aiofiles.open(file_name, mode="r") as f:
                body = await f.read()
                return MarketplaceListing.schema().loads(body, many=True)
        else:
            return []

    async def save_listings(self, listings: list[MarketplaceListing]) -> None:
        """Saves the provided MarketplaceItems as processed."""
        file_name = f"listing_data/{self.name}{self.search_term}.json"
        async with aiofiles.open(file_name, mode="w") as f:
            await f.write(MarketplaceListing.schema().dumps(listings, many=True))

    def log(self, message: str) -> None:
        print(f"[{self.name}] {message}")

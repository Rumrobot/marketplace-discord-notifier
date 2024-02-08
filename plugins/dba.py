import html
import json
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from .common import MarketplaceListing, MarketplacePlugin


class Plugin(MarketplacePlugin):
    def __init__(self, session: ClientSession, search_url: str) -> None:
        name = "DBA"
        color = 0x010C8D
        super().__init__(name, color, session, search_url)

    async def fetch_listings(self):
        existing_listings = await self.get_saved_listings()
        try:
            response = await self.session.get(self.search_url)
        except Exception as e:
            self.log(f"Error when requesting DBA site: {e}")
            return []
        text = await response.text()

        # Parse HTML
        soup = BeautifulSoup(text, "html.parser")
        scripts = soup.find_all("script", {"type": "application/ld+json"})

        listings = []
        for script in scripts:
            text = html.unescape(html.unescape(script.string)).replace("\n", "")
            try:
                json_data = json.loads(text)
            except json.JSONDecodeError as e:
                self.log(f"Error decoding JSON: {e}")
                return []

            name = json_data.get("name")
            image_url = json_data.get("image").split("?")[0] + "?class=S1600X1600"
            url = json_data.get("url")
            price = json_data.get("offers", {}).get("price")

            if url not in [listing.url for listing in existing_listings]:
                listings.append(
                    MarketplaceListing(name, image_url, url, f"{int(price):,d} kr")
                )

        await self.save_listings(existing_listings + listings)
        return listings  # The new ones

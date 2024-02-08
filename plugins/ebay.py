import html
import json
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from .common import MarketplaceListing, MarketplacePlugin


class Plugin(MarketplacePlugin):
    def __init__(self, session: ClientSession, search_url: str) -> None:
        name = "eBay"
        color = 0xFBCD25
        super().__init__(name, color, session, search_url)

    async def fetch_listings(self):
        existing_listings = await self.get_saved_listings()
        try:
            response = await self.session.get(self.search_url)
        except Exception as e:
            self.log(f"Error when requesting site: {e}")
            return []
        text = await response.text()

        # Parse HTML
        soup = BeautifulSoup(text, "html.parser")
        list_items = soup.find(
            "ul", {"class": "srp-results srp-list clearfix"}
        ).find_all("li", recursive=False)

        listings = []
        for item in list_items:
            if "s-item" in item.get("class", []):
                url = item.find("a", {"class": "s-item__link"}).get("href", "").split("?")[0]
                name = item.find("div", {"class": "s-item__title"}).text
                image_url = item.find("img").get("src")
                price = item.find("span", {"class": "s-item__price"}).text
                if url not in [listing.url for listing in existing_listings]:
                    listings.append(MarketplaceListing(name, image_url, url, price))
            elif "srp-river-answer--REWRITE_START" in item.get("class", []):
                break

        await self.save_listings(existing_listings + listings)
        return listings  # The new ones

import html
import json
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from .common import MarketplaceListing, MarketplacePlugin


class Plugin(MarketplacePlugin):
    def __init__(self, session: ClientSession, search_url: str) -> None:
        name = "Kleinanzeigen"
        color = 0xB5E941
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
        list_items = soup.find_all("li")

        listings = []

        for item in list_items:
            article = item.find("article", class_="aditem")
            if article:
                name = article.find("h2").text.strip()
                if article.find("img"):
                    image_url = (
                        article.find("img").get("src", "").split("?")[0]
                        + "?rule=$_57.JPG"
                    )
                else:
                    image_url = "https://i.imgur.com/8Eixst2.jpeg"
                url = "https://kleinanzeigen.de" + article["data-href"]
                price = (
                    article.find(
                        "p", class_="aditem-main--middle--price-shipping--price"
                    )
                    .text.strip()
                    .split(" €")[0]
                    .replace(".", "")
                )

                if url not in [listing.url for listing in existing_listings]:
                    listings.append(
                        MarketplaceListing(name, image_url, url, f"{int(price):,d} €")
                    )

        await self.save_listings(existing_listings + listings)
        return listings  # The new ones

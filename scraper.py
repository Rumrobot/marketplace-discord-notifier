import asyncio
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import aiohttp
import time
import html

load_dotenv()

DBA_URL = os.getenv("DBA_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DISCORD_ROLE_ID = os.getenv("DISCORD_ROLE_ID")


async def fetch_dba(listings, session):
    # Load existing listings from file
    try:
        with open("listings.json", "r", encoding="utf-8") as f:
            existing_listings = json.load(f)
    except FileNotFoundError:
        print("No existing listings.json found; creating one")
        existing_listings = []

    # Request DBA site
    try:
        response = await session.get(DBA_URL)
    except Exception as e:
        print(f"Error when requesting DBA site: {e}")
        return
    text = await response.text()

    # Parse HTML
    soup = BeautifulSoup(text, "html.parser")
    scripts = soup.find_all("script", {"type": "application/ld+json"})

    for script in scripts:
        # Clean JSON
        json = html.unescape(html.unescape(script.string))
        try:
            # Load data from JSON
            json_data = json.loads(json)

            name = json_data.get("name")
            image_url = json_data.get("image").split("?")[0] + "?class=S1600X1600"
            url = json_data.get("url")
            price = json_data.get("offers", {}).get("price")

            if url not in [listing["url"] for listing in existing_listings]:
                # Store data
                listing_data = {
                    "name": name,
                    "image_url": image_url,
                    "url": url,
                    "price": price,
                }

                listings.append(listing_data)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    all_listings = existing_listings + listings

    # Save new listings to file
    output_file = "listings.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_listings, f, ensure_ascii=False, indent=4)

    return listings


async def discord(listings, session):
    for listing in listings:
        name = listing["name"]
        price = listing["price"]
        image_url = listing["image_url"]
        listing_url = listing["url"]

        # Create request for webhook
        body = {
            "content": f"||<@&{DISCORD_ROLE_ID}>||",
            "embeds": [
                {
                    "color": 0x010C8D,
                    "title": name,
                    "url": listing_url,
                    "fields": [{"name": "Price", "value": f"{int(price):,d} kr"}],
                    "image": {"url": image_url},
                }
            ],
        }
        try:
            response = await session.post(DISCORD_WEBHOOK_URL, json=body)
            print(f"Sent message for {name}")
        except Exception as e:
            print(f"Error while sending webhook message: {e}")
            return


async def main():
    async with aiohttp.ClientSession() as session:
        listings = []

        listings = await fetch_dba(listings, session)
        await discord(listings, session)

        if listings == []:
            print("No new listings found")


if __name__ == "__main__":
    while True:
        asyncio.run(main())

        # Sleep for 1 minute
        time.sleep(60)

import asyncio
from contextlib import suppress
import importlib
from itertools import zip_longest
import json
import aiofiles
from aiofiles import os

from aiohttp import ClientSession
from jsonschema import ValidationError, validate

from plugins.common import MarketplacePlugin
from utils import batched


async def main():
    with suppress(FileExistsError):
        await os.mkdir("listing_data")

    async with ClientSession(
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; x64; en-US) AppleWebKit/602.9 (KHTML, like Gecko) Chrome/55.0.3782.249 Safari/600"
        }
    ) as session:
        schema_resp = await session.get(
            "https://raw.githubusercontent.com/Rumrobot/marketplace-discord-notifier/main/static/schema.json"
        )
        schema = json.loads(await schema_resp.text())
        try:
            async with aiofiles.open("config.json", mode="r") as f:
                config_text = await f.read()
                config = json.loads(config_text)
                validate(instance=config, schema=schema)
        except FileNotFoundError:
            print("No config file found.")
            return
        except ValueError:
            print("Config file contains invalid JSON.")
            return
        except ValidationError as e:
            print(f"Configuration is invalid.\n{e.message}")
            return

        print("Configuration is valid.")

        while True:
            for plugin_config in config["plugins"]:
                try:
                    plugin_module = importlib.import_module(
                        f"plugins.{plugin_config['name']}"
                    )
                    plugin_class = getattr(plugin_module, "Plugin")
                    plugin: MarketplacePlugin = plugin_class(
                        session=session, search_url=plugin_config["search_url"]
                    )
                except ImportError as e:
                    print(f"Error loading plugin: {e}")
                    continue
                except AttributeError as e:
                    print(f"Error loading plugin class: {e}")
                    continue

                print(f"Fetching listings for {plugin_config['name']}...")

                listings = await plugin.fetch_listings()
                if not listings:
                    print(f"No listings found for {plugin_config['name']}.")
                    continue

                for i, batch in enumerate(
                    batched(listings, 10)
                ):  # Group new listings into chunks of 10 (max embeds in one message)
                    embeds = []
                    for listing in batch:
                        embeds.append(
                            {
                                "color": plugin.color,
                                "title": listing.name,
                                "url": listing.url,
                                "fields": [{"name": "Price", "value": listing.price}],
                                "image": {"url": listing.image_url},
                            }
                        )
                    body = {
                        "content": (
                            plugin_config.get("message_content") if i == 0 else None
                        ),
                        "embeds": embeds,
                    }

                    response = await session.post(
                        plugin_config["webhook_url"], json=body
                    )
                    if not response.ok:
                        plugin.log(f"Error while sending message: {response.status}")
                    else:
                        plugin.log(f"Sent message with {len(batch)} new listings.")

            await asyncio.sleep(config["interval"])


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import importlib
import json
import aiofiles
from aiofiles.os import rmdir

from aiohttp import ClientSession
from jsonschema import ValidationError, validate

from plugins.common import MarketplacePlugin


async def main():
    rmdir("listing_data")

    main_loop = True
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
            return print("No config file found.")
        except ValueError:
            return print("Config file contains invalid JSON.")
        except ValidationError as e:
            return print(f"Configuration is invalid.\n{e.message}")

        while main_loop:
            try:
                plugin_module = importlib.import_module("plugins.dba")
                plugin_class = getattr(plugin_module, "Plugin")
                plugin: MarketplacePlugin = plugin_class(
                    session=session, search_term="Test"
                )
                listings = await plugin.fetch_listings()
            except ImportError as e:
                print(f"Error loading plugin: {e}")
            except AttributeError as e:
                print(f"Error loading plugin class: {e}")

            await asyncio.sleep(config["interval"])


if __name__ == "__main__":
    asyncio.run(main())

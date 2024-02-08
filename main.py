import asyncio
import importlib
import json
import aiofiles

from aiohttp import ClientSession
from jsonschema import ValidationError, validate

from plugins.common import MarketplacePlugin


async def main():
    main_loop = True
    async with ClientSession(
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; x64; en-US) AppleWebKit/602.9 (KHTML, like Gecko) Chrome/55.0.3782.249 Safari/600"
        }
    ) as session:
        while main_loop:
            schema_resp = await session.get(
                "https://johnnyjth.com/schema/marketplace-discord-notifier.json"
            )
            schema = await schema_resp.json()
            try:
                async with aiofiles.open("config.json", mode="r") as f:
                    config_text = await f.read()
                    config = json.loads(config_text)
                    validate(instance=config, schema=schema)
            except FileNotFoundError:
                main_loop = False
                return print("No config file found.")
            except ValueError:
                main_loop = False
                return print("Config file contains invalid JSON.")
            except ValidationError as e:
                main_loop = False
                return print(f"Configuration is invalid.\n{e.message}")

            try:
                plugin_module = importlib.import_module("plugins.dba")
                plugin_class = getattr(plugin_module, "Plugin")
                plugin: MarketplacePlugin = plugin_class(
                    session=session, search_term="Test"
                )
                items = await plugin.fetch_items()
            except ImportError as e:
                print(f"Error loading plugin: {e}")
            except AttributeError as e:
                print(f"Error loading plugin class: {e}")

            await asyncio.sleep(config.interval)


if __name__ == "__main__":
    asyncio.run(main())

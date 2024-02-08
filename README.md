# Marketplace Discord Notifier
This is a simple script that notifies you when a new item is added to a search term of your choice on one of the following marketplaces:
Name | URL
--- | ---
Den Blå Avis | https://dba.dk

It uses the [Discord Webhook API](https://discord.com/developers/docs/resources/webhook) to send a message to a channel of your choice.

## Installation
1. Clone the repository
2. Install the requirements
```bash
pip install -r requirements.txt
```
3. Copy the `config.example.json` file and rename it to `config.json`
```bash
copy config.example.json config.json
```
4. Fill in the `config.json` file with your information
5. Run the script
```bash
python main.py
```

## Configuration
The `config.json` file contains the following fields:
- `plugins`: The plugins you want to enable. Multiple of the same plugin can be added (with different search terms).
- `interval`: The interval in seconds between each check for new items.

### Plugins
Each plugin has the following fields:
- `name`: The name of the plugin. This can be one of the following:
  - [`dba`](#dba)
- `search_url`: The URL of the search query you want to monitor. Plugin specific.
- `webhook_url`: The URL of the Discord Webhook you want to send the message to.
- `message_content`: The message you want to be sent to the Discord channel alongside the listings. 
  - For Discord mentions you have to write the mention in a channel and put a backslash before the @ symbol. Example: `\@JohnnyJTH`. When you send the message, it will look something like this: `<@&1001569699735273502>`. You can copy this and paste it into the `message_content` field.

> [!NOTE]
> In most cases, the correct `search_url` can be found by going to the marketplace and searching for the item you want to monitor, with the filters you want. Then copy the URL and paste it into the `search_url` field.

> [!IMPORTANT]
> You should always sort the listings by the newest first for the best results.

#### DBA
For the `dba` plugin, the `search_url` field should be the URL of the search query you want to monitor. For example, if you want to monitor new analogue cameras, the `search_url` field could be `https://www.dba.dk/billede-og-lyd/analoge-kameraer/andre-analoge-kameraer/?sort=listingdate-desc`.

It can also be a normal search query, for example: `https://www.dba.dk/soeg/?soeg=analoge+kameraer&sort=listingdate-desc`. The `sort` parameter is important, as it sorts the listings by the date they were added. The `listingdate-desc` parameter sorts the listings by the date they were added, in descending order. This ensures that the newest listings are always shown first.

#### eBay
For the `ebay` plugin, the `search_url` field should be the URL of the search query you want to monitor. For example, if you want to monitor new analogue cameras, the `search_url` field could be `https://www.ebay.com/sch/i.html?_nkw=analog+camera&_sop=10`. This means that the search query is `analog camera` and the listings are sorted by the newest first.

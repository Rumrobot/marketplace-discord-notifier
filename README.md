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
  - `dba`
- `search_term`: The search term you want to be notified about.
- `webhook_url`: The URL of the Discord Webhook you want to send the message to.
- `message_content`: The message you want to be sent to the Discord channel alongside the listings. 
  - For Discord mentions you have to write the mention in a channel and put a backslash before the @ symbol. Example: `\@JohnnyJTH`. When you send the message, it will look something like this: `<@&1001569699735273502>`. You can copy this and paste it into the `message_content` field.

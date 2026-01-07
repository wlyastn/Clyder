# Clyder: A Discord Data Analysis Tool

I built Clyder to pull and analyze message history from Discord channels without having to manually export or use third-party services. It's useful for keyword searches across time, archival, or understanding conversation trends in a server.

**Important**: Use this only on servers where you have permission to access the data.

## What It Does

- **Fetch Messages**: Pull all messages from a channel, optionally filtered by date range
- **Keyword Search**: Find messages containing specific keywords
- **Export to CSV**: Save results with message ID, timestamp, author, content, and more
- **Flexible Date Handling**: Accepts YYYY-MM-DD format, converts to UTC automatically
- **Rate Limit Aware**: Built-in delays to respect Discord API limits

## Disclaimer

By using this tool, you agree to comply with Discord's Terms of Service. This tool does not perform any scraping activities; instead, it leverages Discord's official API for data retrieval, respecting all rate limits and usage guidelines. Misuse of this tool, such as using it in ways that violate Discord's Terms of Service (e.g., unauthorized data collection, using self-bots), can result in account termination. The creator of this tool does not endorse or encourage any activities that violate Discord's Terms of Service.

## Usage

To use Clyder, you'll need to enable Developer Mode in Discord and gather your authorization token, server ID, and channel ID. Follow the steps below:

![Developer Mode in Discord](images/discorddevelopermode.png)

### Step 1: Enable Developer Mode in Discord

1. Open Discord and go to **User Settings** (gear icon in the bottom-left).
2. Navigate to **Advanced** tab.
3. Enable **Developer Mode**.
4. Close settings.

### Step 2: Obtain Your Authorization Token

1. Open your Discord server in a **Chromium-based browser** (Chrome, Edge, Brave, etc.).
2. Press `F12` to open **Developer Tools**.
3. Go to the **Network** tab.
4. Interact with Discord (scroll through channels, send a message, etc.).
5. In the Network tab's search/filter box, search for:

    ```
    messages?limit=50
    ```

6. Click on the result that appears.
7. Scroll down to **Request Headers** and find the **Authorization** header. It will look like:

    ```
    Authorization: Tl4gh9sd...
    ```

    Copy the entire value after "Authorization: ". This is your **Auth Token**.

![Finding your authorization token](images/messageslimit.png)

### Step 3: Obtain Your Server ID

1. In Discord, right-click on your **server name/icon** (on the left sidebar).
2. Select **"Copy Server ID"** from the context menu.

![Getting your server ID](images/serverid.png)

### Step 4: Obtain Your Channel ID

1. In Discord, right-click on the **channel name** you want to analyze.
2. Select **"Copy Channel ID"** from the context menu.

![Getting your channel ID](images/channelid.png)

### Step 5: Run the Tool

1. Clone the repository and navigate to the project directory:

    ```bash
    git clone <repository-url>
    cd Clyder
    ```

2. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:

    ```bash
    python Clyder.py
    ```

4. Follow the interactive prompts:
   - Enter your Discord bot token
   - Enter your server ID
   - Enter your channel ID
   - Choose to fetch all messages (a) or keyword search (k)
   - Optionally filter by date range
   - If doing keyword search, enter comma-separated keywords

## Exported Data

The tool saves results as CSV with these columns:

```
message_id,timestamp,author_id,author_name,content,channel_id,guild_id,attachments
123456789,2025-01-07T14:23:01.000000+00:00,987654321,alice,\"yo this is cool\",555,666,
123456790,2025-01-07T14:25:15.000000+00:00,111111111,bob,\"totally agree\",555,666,https://cdn.discord.com/attachments/...
```

## Known Quirks

- Large channels (10k+ messages) can take a while—Discord rate limits kick in, but we respect that
- Deleted messages are gone for good (Discord API doesn't return them)
- Embeds and reactions aren't included, just the raw message text
- If a user deletes their account, their author_name shows as "Deleted User" but author_id is preserved

## License

This project is licensed under the [MIT License](./LICENSE).

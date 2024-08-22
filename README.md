# Clyder: A Discord Data Analysis Tool

## Overview

This is a Python-based script designed for analyzing data from Discord servers. It allows users to retrieve messages from specified channels within a server and perform keyword-based searches on those messages. This tool is intended for data analysis purposes and **is not a scraper**. It is built to comply with Discord's Terms of Service, and users should ensure they have the appropriate permissions to access the data they are analyzing.

**Important**: You can only use this tool on servers you own. This tool supports using a bot token or your personal authorization token.

## Features

- **Fetch Messages**: Retrieve all messages from a specified Discord channel within an optional date range.
- **Keyword Search**: Search for specific keywords within the messages of a Discord channel.
- **Data Export**: Save the retrieved data as a CSV file for further analysis.
- **Rate Limit Handling**: Built-in rate limit management to ensure compliance with Discord API limits.

## Disclaimer

By using this tool, you agree to comply with Discord's Terms of Service. This tool does not perform any scraping activities; instead, it leverages Discord's official API for data retrieval, respecting all rate limits and usage guidelines. Misuse of this tool, such as using it in ways that violate Discord's Terms of Service (e.g., unauthorized data collection, using self-bots), can result in account termination. The creator of this tool does not endorse or encourage any activities that violate Discord's Terms of Service.

## Usage

### Step 1: Obtain Your Authorization Token

1. Open your Discord account and enable "Developer Tools" in a Chromium-based browser.
2. Select the "Network" tab.
3. Engage in activity, like clicking around in channels and servers.
4. In the left-hand search box, enter the following text:

    ```bash
    messages?limit=50
    ```

5. Click on the found text and scroll down until you see "Authorization" under "Request Headers". It should look like this:

    ```makefile
    Authorization: Tl4gh9sd...
    ```

    This is your "Auth. Token".

### Step 2: Enable Developer Tools in Discord

Enable "Developer Tools" in your Discord settings, under the "Advanced" tab.

### Step 3: Obtain Server and Channel IDs

- Right-click on the server icon for the "Server ID".
- Right-click on the channel for the "Channel ID".

### Step 4: Run the Tool

Follow the prompts to enter your Discord bot token, server ID, and channel ID.

## Exported Data

The tool will save the retrieved messages or keyword search results to a CSV file in the working directory.

## Keyboard Shortcuts

- **Exit at Any Time**: Press the Escape key to quit the program at any time during its execution.

## Logging

All operations and errors are logged to `app.log` and `error.log` respectively. These logs include timestamps and are useful for debugging or reviewing tool performance.

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

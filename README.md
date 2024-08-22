# Clyder

## Overview

This is a Python-based tool designed for analyzing data from Discord servers. It allows users to retrieve messages from specified channels within a server and perform keyword-based searches on those messages. This tool is intended for data analysis purposes and **is not a scraper**. It is built to comply with Discord's Terms of Service, and users should ensure they have the appropriate permissions to access the data they are analyzing.

## Features

- **Fetch Messages**: Retrieve all messages from a specified Discord channel within an optional date range.
- **Keyword Search**: Search for specific keywords within the messages of a Discord channel.
- **Data Export**: Save the retrieved data as a CSV file for further analysis.
- **Rate Limit Handling**: Built-in rate limit management to ensure compliance with Discord API limits.
- **Error Logging**: Comprehensive logging of errors and warnings to ensure smooth operation and easy debugging.

## Disclaimer

By using this tool, you agree to comply with Discord's Terms of Service. This tool does not perform any scraping activities; instead, it leverages Discord's official API for data retrieval, respecting all rate limits and usage guidelines. Misuse of this tool, such as using it in ways that violate Discord's Terms of Service (e.g., unauthorized data collection, using self-bots), can result in account termination. The creator of this tool does not endorse or encourage any activities that violate Discord's Terms of Service.

## Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/wlyastn/Clyder.git
   cd Clyder
   \`\`\`

2. Set up a virtual environment (optional but recommended):
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   \`\`\`

3. Install the required dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## Usage

1. **Configure Your Bot**: Ensure you have a valid Discord bot token and the necessary permissions to access the server and channels you wish to analyze.

2. **Run the Tool**:
   \`\`\`bash
   python Clyder.py
   \`\`\`

   Follow the prompts to enter your Discord bot token, server ID, and channel ID.

3. **Exported Data**: The tool will save the retrieved messages or keyword search results to a CSV file in the working directory.

### Keyboard Shortcuts

- **Exit at Any Time**: Press the `Escape` key to quit the program at any time during its execution.

## Logging

- All operations and errors are logged to `app.log` and `error.log` respectively.

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

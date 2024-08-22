# Written by wlyastn July 24, 2024
import os
import logging
import requests
import pandas as pd
import time
from datetime import timezone
from dateutil.parser import parse as dateutil_parse
from InquirerPy import prompt

DISCLAIMER = """
By using this tool, you agree to comply with Discord's Terms of Service.
You acknowledge that using self-bots or data scraping is a violation of these
terms and can result in account termination. Use this tool at your own risk.
The creator of this tool does not endorse or encourage any activities that
violate Discord's Terms of Service.
"""

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.FileHandler("error.log"),
        logging.StreamHandler()
    ]
)

def rate_limited_request(url, headers, retries=5):
    """
    Makes a GET request with a rate limit handler.
    Retries the request if a rate limit is encountered.
    Logs errors to an error file.
    """
    for i in range(retries):
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r
        elif r.status_code == 429:
            retry_after = int(r.headers.get("Retry-After", 1))
            logging.warning(f"Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
        else:
            logging.error(f"Failed to fetch data from {url}. Status code {r.status_code}")
            r.raise_for_status()
    raise Exception(f"Failed to fetch data from {url} after {retries} retries")

def get_server_name(server_id, headers):
    """
    Fetches the server name using the server ID.
    Logs an error if the server cannot be found.
    """
    try:
        url = f'https://discord.com/api/v9/guilds/{server_id}'
        r = rate_limited_request(url, headers)
        server_info = r.json()
        return server_info.get('name', 'Unknown Server')
    except request.exceptions.RequestException as e:
        logging.error(f"Error fetching server name: {e}")
        return None

def get_channel_name(channel_id, headers):
    """
    Fetches the channel name using the channel ID.
    Logs an error if the channel cannot be found.
    """
    url = f'https://discord.com/api/v9/channels/{channel_id}'
    try:
        r = rate_limited_request(url, headers)
        channel_info = r.json()
        return channel_info.get('name', 'Unknown Channel')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching channel name :{e}")
        return None

def get_approximate_member_count(server_id, headers):
    """
    Fetches the approximate online presence count of the server.
    Logs an error if the count cannot be fetched.
    """
    try:
        r = rate_limited_request(f'https://discord.com/api/v9/guilds/{server_id}/preview', headers)
        j = r.json()
        return j.get('approximate_member_count', 'Key not found')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching member count: {e}")
        return 'Error'

def get_approximate_presence_count(server_id, headers):
    """
    Fetches the approximate online presence count of the server.
    Logs an error if the count cannot be fetched.
    """
    try:
        r = rate_limited_request(f'https://discord.com/api/v9/guilds/{server_id}/preview', headers)
        j = r.json()
        return j.get('approximate_presence_count', 'Key not found')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching presence count: {e}")
        return 'Error'

def filter_messages_by_date(messages, start_date, end_date):
    """
    Filters messages based on provided start and end dates.
    """
    if not start_date and not end_date:
        return messages

    if start_date:
        start_date = dateutil_parse(str(start_date)).replace(tzinfo=timezone.utc)
    if end_date:
        end_date = dateutil_parse(str(end_date)).replace(tzinfo=timezone.utc)

    filtered_messages = []
    for message in messages:
        message_date = dateutil_parse(message['timestamp']).astimezone(timezone.utc)  # Ensure message_date is offset-aware
        if start_date and message_date < start_date:
            continue
        if end_date and message_date > end_date:
            continue
        filtered_messages.append(message)
    return filtered_messages

def is_message_within_date_range(message_date_str, start_date=None, end_date=None):
    """
    Filters messages based on the provided start and end dates.
    """
    message_date = dateutil_parse(message_date_str).replace(tzinfo=timezone.utc)
    if start_date and message_date < start_date:
        return False
    if end_date and message_date > end_date:
        return False
    return True

def get_messages_from_channel(channel_id, server_id, headers, start_date=None, end_date=None):
    """
    Retrieves all messages from a specified channel within an optional date range.
    Logs errors if no messages are found.
    """
    messages = []
    last_message_id = None
    server_name = get_server_name(server_id, headers)
    channel_name = get_channel_name(channel_id, headers)

    if server_name is None or channel_name is None:
        logging.error("Server or channel not found. Aborting message retrieval.")
        return []

    if start_date:
        start_date = dateutil_parse(str(start_date)).replace(tzinfo=timezone.utc)
    if end_date:
        end_date = dateutil_parse(str(end_date)).replace(tzinfo=timezone.utc)

    while True:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=100'
        if last_message_id:
            url += f'&before={last_message_id}'

        r = rate_limited_request(url, headers)
        new_messages = r.json()
        if not new_messages:
            break

        filtered_batch = filter_messages_by_date(new_messages, start_date, end_date)
        if not filtered_batch:
            break

        messages.extend(filtered_batch)
        last_message_id = new_messages[-1]['id']
        if start_date and not is_message_within_date_range(new_messages[-1]['timestamp'], start_date, end_date):
            break

        time.sleep(0.02)  # 50 requests per second limit

    result = []
    for c in messages:
        message = {
            'Server ID': server_id,
            'Server Name': server_name,
            'Channel ID': c['channel_id'],
            'Channel Name': channel_name,
            'Timestamp': c['timestamp'],
            'Author': c['author']['username'],
            'Content': c['content']
        }
        result.append(message)
    if not result:
        logging.warning('No messages found in specified channel or date range.')
    return result

def get_keyword_messages_from_channel(channel_id, server_id, keywords, headers, start_date=None, end_date=None):
    """
    Retrieves messages containing specified keywords from a channel within an optional date range.
    Logs errors if no keyword messages are found.
    """

    messages = []
    last_message_id = None
    server_name = get_server_name(server_id, headers)
    channel_name = get_channel_name(channel_id, headers)

    if start_date:
        start_date = dateutil_parse(str(start_date)).replace(tzinfo=timezone.utc)
    if end_date:
        end_date = dateutil_parse(str(end_date)).replace(tzinfo=timezone.utc)

    while True:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=100'
        if last_message_id:
            url += f'&before={last_message_id}'

        r = rate_limited_request(url, headers)
        new_messages = r.json()
        if not new_messages:
            break

        filtered_batch = filter_messages_by_date(new_messages, start_date, end_date)
        if not filtered_batch:
            break

        for message in filtered_batch:
            if any(keyword.lower() in message['content'].lower() for keyword in keywords):
                messages.append({
                    'Server ID': server_id,
                    'Server Name': server_name,
                    'Channel ID': message['channel_id'],
                    'Channel Name': channel_name,
                    'Timestamp': message['timestamp'],
                    'Author': message['author']['username'],
                    'Content': message['content']
                })

        last_message_id = new_messages[-1]['id']
        if start_date and not is_message_within_date_range(new_messages[-1]['timestamp'], start_date, end_date):
            break

        time.sleep(0.02)  # 50 requests per second limit

    if not messages:
        logging.warning("No keyword messages found in specified channel and date range.")
    return messages

def save_to_csv(messages, filename):
    """
    Saves the retrieved messages to a CSV file.
    Logs the action performed.
    """
    if messages:
        df = pd.DataFrame(messages)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        logging.warning("No data availible to save to CSV.")

def quit_if_esc_pressed():
    if keyboard.is_pressed('esc'):
        logging.info("Escape pressed")
        print("Exiting..")
        exit(0)

def main():
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    print(DISCLAIMER)

    while True:
        # Step 1: Collect bot token, server ID, and channel ID
        questions = [
            {"type": "input", "message": "Enter your Discord bot authorization token:", "name": "bot_token"},
            {"type": "input", "message": "Enter the Discord server ID:", "name": "server_id"},
            {"type": "input", "message": "Enter the Discord channel ID:", "name": "channel_id"}
        ]
        answers = prompt(questions)
        bot_token = answers['bot_token'].strip()
        server_id = answers['server_id'].strip()
        channel_id = answers['channel_id'].strip()

        headers = {'authorization': bot_token}

        # Fetch and display member count and presence count
        member_count = get_approximate_member_count(server_id, headers)
        presence_count = get_approximate_presence_count(server_id, headers)

        print(f"\nApproximate Member Count: {member_count}")
        print(f"Approximate Presence Count: {presence_count}\n")

        # Step 2: Display options to the user
        options = [
            {"type": "list", "message": "Select an action:", "name": "action", "choices": [
                "Get Messages",
                "Get Keyword Messages",
                "Quit"
            ]}
        ]
        choice = prompt(options)['action']

        if choice == "Get Messages":
            start_date = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ")
            end_date = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ")
            messages = get_messages_from_channel(channel_id, server_id, headers, start_date, end_date)
            save_to_csv(messages, 'messages.csv')

        elif choice == "Get Keyword Messages":
            keywords = input("Enter keywords (comma-separated): ").split(',')
            start_date = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ")
            end_date = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ")
            messages = get_keyword_messages_from_channel(channel_id, server_id, keywords, headers, start_date, end_date)
            save_to_csv(messages, 'keyword_messages.csv')

        elif choice == "Quit":
            exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An unexpected error occured. {e}")
        print("An error occurred. Please check the error log for details.")

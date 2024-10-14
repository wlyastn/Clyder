# Written by wlyastn Aug 26, 2024
import time
import requests
import pandas as pd
from dateutil.parser import parse as dateutil_parse
from datetime import timezone

def fetch_messages(channel_id, headers, start_date=None, end_date=None):
    """
    Fetches messages from the specified channel. Can be filtered by date range.
    Yields messages as they are retrieved.
    """
    last_message_id = None
    while True:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=100'
        if last_message_id:
            url += f'&before={last_message_id}'
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            break
        new_messages = r.json()
        if not new_messages:
            break
        filtered_batch = filter_messages_by_date(new_messages, start_date, end_date)
        if not filtered_batch:
            break
        for message in filtered_batch:
            yield message
        last_message_id = new_messages[-1]['id']
        if start_date and not is_message_within_date_range(new_messages[-1]['timestamp'], start_date, end_date):
            break
        time.sleep(0.02)  # 50 requests per second limit

def filter_messages_by_date(messages, start_date, end_date):
    """
    Filters messages based on provided start and end dates.
    """
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
    Checks if the message date is within the provided start and end dates.
    """
    message_date = dateutil_parse(message_date_str).replace(tzinfo=timezone.utc)
    if start_date and message_date < start_date:
        return False
    if end_date and message_date > end_date:
        return False
    return True

def save_to_csv(messages, filename):
    """
    Saves the retrieved messages to a CSV file.
    Logs the action performed.
    """
    if messages:
        df = pd.DataFrame(messages)
        df.to_csv(filename, index=False)
        print(f"\nData saved to {filename}")
    else:
        print("\nNo data available to save to CSV. Please check the log for details.")
        logging.warning("No data available to save to CSV.")

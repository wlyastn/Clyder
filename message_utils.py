# Written by wlyastn Aug 26, 2024
import requests
import time
import csv
from dateutil.parser import parse as dateutil_parse
from datetime import timezone

def fetch_messages(channel_id, headers, start_date=None, end_date=None):
    """
    Fetches messages, optionally filtered by date range.
    """
    last_message_id = None
    while True:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100"
        if last_message_id:
            url += f"&before={last_message_id}"
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"Failed to fetch messages (status {r.status_code}). Stopping.")
            break

        batch = r.json()
        if not batch:
            break

        filtered_batch = filter_messages_by_date(batch, start_date, end_date)
        if not filtered_batch:
            break

        for msg in filtered_batch:
            yield msg

        last_message_id = batch[-1]['id']
        # Check if the last batch is still in the date range
        if start_date and not is_message_within_date_range(batch[-1]['timestamp'], start_date, end_date):
            break

        time.sleep(0.02)

def filter_messages_by_date(messages, start_date, end_date):
    out = []
    for m in messages:
        ts = dateutil_parse(m['timestamp']).astimezone(timezone.utc)
        if start_date and ts < start_date:
            break
        if end_date and ts > end_date:
            continue
        out.append(m)
    return out

def is_message_within_date_range(ts_str, start_date=None, end_date=None):
    ts = dateutil_parse(ts_str).astimezone(timezone.utc)
    if start_date and ts < start_date:
        return False
    if end_date and ts > end_date:
        return False
    return True

def save_to_csv(messages, filename):
    """
    Saves messages to a CSV file.
    """
    if not messages:
        print("No messages to save.")
        return
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=messages[0].keys())
        writer.writeheader()
        writer.writerows(messages)
    print(f"Saved {len(messages)} messages to {filename}")
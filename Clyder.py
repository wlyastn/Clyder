# Written by wlyastn Aug 26, 2024
import os
import time
from datetime import datetime, timezone
from server_utils import (
    get_server_name,
    get_channel_name,
    get_approximate_member_count,
    get_approximate_presence_count
)
from message_utils import fetch_messages, save_to_csv
from dateutil.parser import parse as dateutil_parse, ParserError

DISCLAIMER = """
By using this tool, you agree to comply with Discord's Terms of Service.
Self-bots or scraping can violate Discord's Terms.
Use this at your own risk.
"""

def clear_console():
    """
    Clears the console and displays the disclaimer message
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(DISCLAIMER)

def parse_date_input(date_input):
    """
    Parses user date input and returns a UTC datetime object.
    Returns None if input is empty or invalid.
    """
    date_input = date_input.strip()
    if not date_input:
        return None
    try:
        dt = dateutil_parse(date_input)
        # Ensure UTC if no timezone info
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ParserError:
        print(f"Invalid date '{date_input}', ignoring.")
        return None

def main():
    """
    Main application loop. Prompts user for Discord credentials and fetches messages
    from a specified channel, with optional filtering by keywords or date range.
    """
    while True:
        clear_console()
        bot_token = input("Enter your Discord bot authorization token: ").strip()
        server_id = input("Enter the Discord server ID: ").strip()
        channel_id = input("Enter the Discord channel ID: ").strip()
        if not bot_token or not server_id or not channel_id:
            print("All fields are required. Restarting...\n")
            time.sleep(2)
            continue

        headers = {'authorization': bot_token}

        # Fetch server info
        server_name = get_server_name(server_id, headers)
        channel_name = get_channel_name(channel_id, headers)
        member_count = get_approximate_member_count(server_id, headers)
        presence_count = get_approximate_presence_count(server_id, headers)

        if not server_name or not channel_name or member_count == 'Error' or presence_count == 'Error':
            print("\nFailed to retrieve server/channel data. Check IDs/token.\n")
            time.sleep(2)
            continue

        clear_console()
        print(f"Server: {server_name} (Approx. {member_count} members, {presence_count} online)")
        print(f"Channel: {channel_name}")

        action = input("\nGet all messages (a) / Get keyword messages (k) / Quit (q): ").lower()
        if action == 'q':
            print("Exiting...")
            break

        start_date = parse_date_input(input("\nEnter start date (YYYY-MM-DD) or press Enter to skip: "))
        end_date = parse_date_input(input("Enter end date (YYYY-MM-DD) or press Enter to skip: "))

        keywords = []
        if action == 'k':
            keywords = [k.strip().lower() for k in input("Enter comma-separated keywords: ").split(',') if k.strip()]

        collected = []
        print("\nFetching messages...\n")
        try:
            count = 0
            for msg in fetch_messages(channel_id, headers, start_date, end_date):
                if action == 'k' and not any(kw in msg['content'].lower() for kw in keywords):
                    continue
                collected.append(msg)
                count += 1
                if count % 50 == 0:
                    print(f"  Retrieved {count} messages...")
        except KeyboardInterrupt:
            print("\nInterrupted by user.")

        filename = "keyword_messages.csv" if action == 'k' else "messages.csv"
        save_to_csv(collected, filename)
        print(f"\nSaved {len(collected)} messages to {filename}. Returning to menu...")
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")
#Written by wlyastn Aug 26, 2024
import os
import logging
import time
import itertools
from datetime import datetime, timezone
from InquirerPy import prompt
from server_utils import get_server_name, get_channel_name, get_approximate_member_count, get_approximate_presence_count
from message_utils import fetch_messages, save_to_csv
from dateutil.parser import parse as dateutil_parse, ParserError

DISCLAIMER = """
By using this tool, you agree to comply with Discord's Terms of Service.
You acknowledge that using self-bots or data scraping is a violation of these
terms and can result in account termination. Use this tool at your own risk.
The creator of this tool does not endorse or encourage any activities that
violate Discord's Terms of Service.
\nPress Ctrl+C at any time to quit.
"""

# Generate a timestamped log filename
log_filename = datetime.now().strftime("error_log_%Y%m%d_%H%M%S.log")

# Set up logging to write to a timestamped file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename)
    ]
)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(DISCLAIMER)

def parse_date_input(date_input, date_type):
    """
    Parses the date input provided by the user and returns a datetime object.
    Re-prompts the user if the date is invalid.
    """
    while True:
        if date_input:
            try:
                return dateutil_parse(date_input).replace(tzinfo=timezone.utc)
            except ParserError:
                date_input = input(f"Invalid {date_type} date format. Please use YYYY-MM-DD: ").strip()
        else:
            return None

def spinner():
    """
    Creates a simple spinner for real-time feedback.
    """
    while True:
        for cursor in itertools.cycle(['|', '/', '-', '\\']):
            yield cursor

def main():
    while True:
        clear_console()

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

        if not bot_token or not server_id or not channel_id:
            print("\nAll fields are required. Restarting...\n")
            time.sleep(2)
            continue

        headers = {'authorization': bot_token}

        try:
            # Fetch and display member count and presence count
            member_count = get_approximate_member_count(server_id, headers)
            presence_count = get_approximate_presence_count(server_id, headers)

            if member_count == 'Error' or presence_count == 'Error':
                print("\nUnable to retrieve server information. Please check your input and try again.")
                time.sleep(2)
                continue

            server_name = get_server_name(server_id, headers)
            channel_name = get_channel_name(channel_id, headers)

            if not server_name or not channel_name:
                print("\nUnable to retrieve server or channel information. Please check your input and try again.")
                time.sleep(2)
                continue

            clear_console()

            print(f"\nServer: {server_name}")
            print(f"Channel: {channel_name}")
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
                start_date_input = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ").strip()
                end_date_input = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ").strip()
                start_date = parse_date_input(start_date_input, "start")
                end_date = parse_date_input(end_date_input, "end")

                messages = []
                spinner_gen = spinner()
                print("\nFetching messages...\n")

                for message in fetch_messages(channel_id, headers, start_date, end_date):
                    messages.append(message)
                    print(f"\r{next(spinner_gen)} Gathered {len(messages)} messages", end='', flush=True)

                save_to_csv(messages, 'messages.csv')
                print(f"\n\nFinished fetching {len(messages)} messages.\n")

            elif choice == "Get Keyword Messages":
                keywords = input("Enter keywords (comma-separated): ").split(',')
                start_date_input = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ").strip()
                end_date_input = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ").strip()
                start_date = parse_date_input(start_date_input, "start")
                end_date = parse_date_input(end_date_input, "end")

                messages = []
                spinner_gen = spinner()
                print("\nFetching keyword messages...\n")

                for message in fetch_messages(channel_id, headers, start_date, end_date):
                    if any(keyword.lower() in message['content'].lower() for keyword in keywords):
                        messages.append(message)
                        print(f"\r{next(spinner_gen)} Gathered {len(messages)} keyword messages", end='', flush=True)

                save_to_csv(messages, 'keyword_messages.csv')
                print(f"\n\nFinished fetching {len(messages)} keyword messages.\n")

            elif choice == "Quit":
                print("Exiting...")
                break  # Exit the while loop and terminate the program

        except KeyboardInterrupt:
            print("\nExiting...")
            break

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            print("\nAn error occurred. Please check the log for details.\n")
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
        print("\nExiting...")
        exit(0)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print("An error occurred. Please check the log for details.\n")

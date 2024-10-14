# Written by wlyastn Aug 26, 2024
import requests
import logging

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
        if r.status_code == 200 and 'name' in server_info:
            return server_info['name']
        else:
            print(f"Server ID {server_id} is invalid or not found. Please check the log for details.")
            logging.warning(f"Server ID {server_id} is invalid or not found.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching server name: {e}")
        return None

def get_channel_name(channel_id, headers):
    """
    Fetches the channel name using the channel ID.
    Logs an error if the channel cannot be found.
    """
    try:
        url = f'https://discord.com/api/v9/channels/{channel_id}'
        r = rate_limited_request(url, headers)
        channel_info = r.json()
        if r.status_code == 200 and 'name' in channel_info:
            return channel_info['name']
        else:
            print(f"Channel ID {channel_id} is invalid or not found. Please check the log for details.")
            logging.warning(f"Channel ID {channel_id} is invalid or not found.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching channel name: {e}")
        return None

def get_approximate_member_count(server_id, headers):
    """
    Fetches the approximate member count of the server.
    Logs an error if the count cannot be fetched.
    """
    try:
        r = rate_limited_request(f'https://discord.com/api/v9/guilds/{server_id}/preview', headers)
        j = r.json()
        if r.status_code == 200 and 'approximate_member_count' in j:
            return j['approximate_member_count']
        else:
            print(f"Unable to fetch member count for server ID {server_id}. Please check the log for details.")
            logging.warning(f"Unable to fetch member count for server ID {server_id}.")
            return 'Error'
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
        if r.status_code == 200 and 'approximate_presence_count' in j:
            return j['approximate_presence_count']
        else:
            print(f"Unable to fetch presence count for server ID {server_id}. Please check the log for details.")
            logging.warning(f"Unable to fetch presence count for server ID {server_id}.")
            return 'Error'
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching presence count: {e}")
        return 'Error'

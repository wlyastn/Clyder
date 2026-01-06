# Written by wlyastn Aug 26, 2024
import requests
import time

def rate_limited_request(url, headers, retries=5):
    """
    Makes a GET request with a rate limit handler
    Retries if rate-limited or on transient errors
    """
    for _ in range(retries):
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r
        elif r.status_code == 429:
            retry_after = int(r.headers.get("Retry-After", 1))
            print(f"Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
        else:
            print(f"Failed to fetch data (status {r.status_code}): {url}")
            time.sleep(1)
    raise Exception(f"Failed to fetch data from {url} after {retries} retries")

def get_server_name(server_id, headers):
    try:
        url = f"https://discord.com/api/v9/guilds/{server_id}"
        r = rate_limited_request(url, headers)
        return r.json().get('name')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching server name: {e}")
        return None

def get_channel_name(channel_id, headers):
    try:
        url = f"https://discord.com/api/v9/channels/{channel_id}"
        r = rate_limited_request(url, headers)
        return r.json().get('name')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching channel name: {e}")
        return None

def get_approximate_member_count(server_id, headers):
    try:
        url = f'https://discord.com/api/v9/guilds/{server_id}/preview'
        r = rate_limited_request(url, headers)
        return r.json().get('approximate_member_count', 'Error')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching member count: {e}")
        return 'Error'

def get_approximate_presence_count(server_id, headers):
    try:
        url = f'https://discord.com/api/v9/guilds/{server_id}/preview'
        r = rate_limited_request(url, headers)
        return r.json().get('approximate_presence_count', 'Error')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching presence count: {e}")
        return 'Error'
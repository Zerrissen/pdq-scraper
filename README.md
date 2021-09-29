# PDQ Scraper
###### Scrapes a list of vulnerable PDQ carwasher control portals, and outputs them to JSON format. Not intended for illegal use. Developers are not held responsible for the use of this program.

## Installation
Tested on Python 3.8.10 Ubuntu 20.04.3

Before running the program, run:
```
pip install -r requirements.txt
```

If this does not work, please manually install the following modules:
```
pip install requests
pip install shodan
```
Make sure to add your Shodan API key to the program! It's on line 9 if you're hella blind.

## Usage
Pretty simple:
```
python3 pdqscraper.py -u USER -p PASSW
```

- Valid IP addresses that successfully log in will be outputted to a JSON file
- Invalid credentials are not logged to keep the JSON clean

## Note
This script does not have an API limit, be careful how much you use it as you may use up your monthly Shodan search limit.

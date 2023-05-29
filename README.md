# PDQ Scraper

###### Scrapes a list of vulnerable PDQ carwasher control portals, and outputs them in plaintext on an HTML page. Not intended for illegal use. Developers are not held responsible for the use of this program.

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
pip install redis
pip install python-dotenv
pip install flask
```

You will also need to create a .env file in the root of the project with the following variables:

```
REDIS_URL=<Redis Connection URL>
REDIS_PORT=<Redis Connection Port
REDIS_PASSWORD=<Redis DB Password>
```

This is required as the client listens for events from the database when querying Shodan, to update the frontend.

## Usage

1. Start up the application server

```
python3 app.py
```

2. Open your browser and navigate to `http://127.0.0.1:5000`

3. Enter your Shodan API key into "Shodan API Key" field.

4. Enter the username and password to test with. THIS IS NOT YOUR SHODAN DETAILS!

5. Select the number of pages you want to pull from Shodan. Note that the more pages, the more API credit this will use against your API key. I recommend starting with 1 page to begin with.
6. The server will start a background process to query Shodan and test the credentials you provided. It will return valid responses to the client and slowly add them to the textarea on the HTML page.

## Note

This program is intended for educational purposes only. The developer of this program is not responsible for any legal ramifications that may be involved with misusing this program.

## License

This repository is licensed under the GNU Affero General Public License v.30.
Permissions of this strongest copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights. When a modified version is used to provide a service over a network, the complete source code of the modified version must be made available.

Read more [here](https://github.com/Zerrissen/pdq-scraper/blob/main/LICENSE)

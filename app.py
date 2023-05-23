import json
import time

import requests
import shodan
from flask import Flask, json, render_template, request
from requests.models import HTTPBasicAuth

def call_api(api, query, user, passw, pageCount):
    # get all pages from pageCount
    page = 1
    pages = []
    while page <= int(pageCount):
        print('doing things')
        try:
            pages.append(api.search(query, page=page))
            page += 1
        except shodan.APIError as e:
            print(f'Error: {e}')
            return [e] # return as list due to html template looking for iterable
    # filter through all pages/test creds
    instanceResults = []
    for instance in pages():
        for match in instance:
            try:
                print(match)
                res = requests.get(f'https://{user}:{passw}@{match["ip_str"]}:{match["port"]}')
                if res.status_code == 200: # successful
                    instanceResults.append(match)
                    #textResults.append('http://' + user + ':' + passw + '@' + instance['ip_str'] + ':' + str(instance['port']))
            except requests.exceptions.ConnectionError as e:
                print(f'Connection Error: {e}')

    # return results
    jsonInstanceResults = json.dumps(instanceResults)
    return jsonInstanceResults

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST', 'GET'])
def scrape():
    if request.method == 'GET':
        return index()
    else:
        api_key = request.form['shodan-api-key']
        api = shodan.Shodan(api_key)
        query = 'WWW-Authenticate: Basic Realm="PDQ"'
        user = request.form['username']
        passw = request.form['password']
        pageCount = request.form['page-count']
        return render_template('index.html', query_results=call_api(api, query, user, passw, pageCount))

if __name__ == '__main__':
    app.run(debug=True)
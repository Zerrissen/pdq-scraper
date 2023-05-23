from flask import Flask, render_template, request, json

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
        return render_template('index.html', api_key=api_key)

def handle_data():
    return json.dumps({'api_key': request.form['shodan-api-key-input']})

if __name__ == '__main__':
    app.run(debug=True)
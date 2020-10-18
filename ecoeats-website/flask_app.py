# Flask App
import logging, json
from flask import Flask, request, render_template, Response
from TestScraper import searchDataSet
from processor import Processor

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/table')
def about():
    return render_template('table.html')

# Test Flask API endpoint below

@app.route('/api', methods=['GET', 'POST'])
def api():

    # uses GET as we use arguments in the URL
    if request.method == 'POST':
        title = request.args.get('title')
        ingredients = request.args.get('ingredients')
        data = searchDataSet(title, ingredients)
        r = Response(json.dumps(data))
        r.headers['Access-Control-Allow-Origin'] = '*'
        return r
    elif request.method == 'GET':
        data = searchDataSet("apple", "")
        r = Response(json.dumps(data))
        r.headers['Access-Control-Allow-Origin'] = '*'
        return r

# Notice: Consider that for a get request, the maxiumum url length is 2048 characters, including the arguments

@app.route('/search', methods=['GET', 'POST'])
def search():

    data_path = '/home/caaatdubhacks/ecoeats/static/Food_Production.csv'
    logging_level = logging.INFO
    proc = Processor(logging_level, data_path)

    if request.method == 'POST':
        title = request.args.get('title')
        ingredients = request.args.get('ingredients')
        request_data = {}
        request_data["title"] = title
        request_data["ingredients"] = ingredients
        r = proc.get_json_match(proc.df, request_data)
        r = Response(r)
        r.headers['Content-Type'] = 'text/plain'
        r.headers['Access-Control-Allow-Origin'] = '*'
        r.headers['Access-Control-Allow-Headers'] = '*'
        r.headers['Access-Control-Allow-Methods'] = '*'
        return r
    if request.method == 'GET':
        title = request.args.get('title')
        ingredients = request.args.get('ingredients')
        request_data = {}
        request_data["title"] = title
        request_data["ingredients"] = ingredients

        r = proc.get_json_match(proc.df, request_data)
        r = Response(r)
        # Cross-origin resource sharing is a mechanism that allows restricted resources on a web page to be requested from another domain outside the domain
        # from which the first resource was served. A web page may freely embed cross-origin images, stylesheets, scripts, iframes, and videos.
        r.headers['Content-Type'] = 'text/plain' # cors only allows for application/x-www-form-urlencoded, multipart/form-data, and text/plain
        r.headers['Access-Control-Allow-Origin'] = '*'
        r.headers['Access-Control-Allow-Headers'] = '*'
        r.headers['Access-Control-Allow-Methods'] = '*'
        return r

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


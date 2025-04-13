from flask import Flask, jsonify, send_from_directory
import json
import os

app = Flask(__name__, static_folder='../src', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/pages/<path:path>')
def serve_pages(path):
    return send_from_directory(os.path.join(app.static_folder, 'pages'), path)

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), path)

@app.route('/api/events')
def get_events():
    with open('data/events.json') as f:
        events = json.load(f)
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)


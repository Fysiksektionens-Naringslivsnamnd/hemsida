from flask import Flask, jsonify, send_from_directory, request, redirect, render_template
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
    # could database or other data source
    with open('data/events.json') as f:
        events = json.load(f)
    return jsonify(events)

@app.route('/pages/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        #TODO: This info needs to be sent to designated email and saved to storage

        return redirect("/index.html") # Redirect to a thank you page or similar

    return redirect('index.html')


if __name__ == '__main__':
    app.run(debug=True)


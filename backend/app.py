from flask import Flask, jsonify, send_from_directory, request, redirect, render_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import sqlite3
import smtplib
import json
import os
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = ''
SMTP_PORT = None
SMTP_USER = ''  # will need to create a designated adress for this
SMTP_PASSWORD = os.getenv("SMTP_PW")
TO_EMAIL = ''  # this will be set to the FN email

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
    data_path = Path(__file__).parent / 'data' / 'events.json'
    with open('data/events.json') as f:
        events = json.load(f)
    return jsonify(events)

@app.route('/pages/contact', methods=['GET'])
def alumni_form():
    raise NotImplementedError("This function is not implemented.")
    if request.method == 'GET':
        name = request.form['name']
        email = request.form['email']
        user_type = request.form['user_type'] # alumni or student
        # TODO: determine details with head of alumni
        with sqlite3.connect('data/alumni.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alumni (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    user_type TEXT
                )
            ''')
            cursor.execute('''
                INSERT INTO alumni (name, email, user_type)
                VALUES (?, ?, ?)
            ''', (name, email, user_type))
            conn.commit()


@app.route('/pages/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['msg']

        # should this also be saved to db?
        subject = "New Contact Form Submission"
        body = f"""
                You have received a new message from your website contact form:

                Name: {name}
                Email: {email}
                Message:
                {message}
                """
        # send_email(subject, body)

        #TODO: This info needs to be sent to designated email and saved to storage

        return redirect("/index.html") # Redirect to a thank you page or similar

    return redirect('index.html')

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    # Connect and send
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Upgrade the connection to secure
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


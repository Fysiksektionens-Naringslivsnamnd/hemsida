from flask import Flask, jsonify, send_from_directory, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import sqlite3
import smtplib
import json
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
load_dotenv()




SMTP_SERVER = ''
SMTP_PORT = None
SMTP_USER = ''  # will need to create a designated adress for this
SMTP_PASSWORD = os.getenv("SMTP_PW")
TO_EMAIL = ''  # this will be set to the FN email

# Absolute path to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'static'),        # ⬅️ points to /static
    static_url_path='/static',                             # ⬅️ URLs start with /static
    template_folder=os.path.join(BASE_DIR, 'src/pages')    # ⬅️ HTML lives here
)


@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route("/contact")
def serve_contact(): 
    return render_template('contact.html')

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



# For database
# === Configuration ===
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# === Model ===
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(300))

    
# === Routes ===
@app.route('/admin', methods=['GET'])
def admin():
    events = Event.query.all()
    return render_template('admin.html', events=events)


@app.route('/admin/add-event', methods=['POST'])
def add_event():
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # ✅ Get form fields
    title = request.form['title']
    date = request.form['date']
    description = request.form['description']
    link = request.form['link']

    # ✅ Handle file upload
    file = request.files['image_file']
    if file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image_url = f'/static/uploads/{filename}'
    else:
        image_url = ''  # or set a default image path

    # ✅ Save to DB
    new_event = Event(title=title, date=date, description=description, image=image_url, link=link)
    db.session.add(new_event)
    db.session.commit()

    return redirect('/admin')


@app.route('/admin/delete-event', methods=['POST'])
def delete_event():
    event_id = request.form['id']
    event = Event.query.get(event_id)
    if event:
         # 🔥 Try deleting the associated image file
        if event.image and event.image.startswith('/static/uploads/'):
            # Build the full path from the relative URL
            image_path = os.path.join(BASE_DIR, event.image.lstrip('/'))
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    print(f"Warning: Could not delete image file: {e}")

                    
        db.session.delete(event)
        db.session.commit()
    return redirect("/admin")


@app.route('/events', methods=['GET'])
def event():
    events = Event.query.all()
    return render_template('events.html', events=events)


if __name__ == '__main__':

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)   
    


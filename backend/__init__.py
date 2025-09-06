import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'static'),        # ⬅️ points to /static
    static_url_path='/static',                             # ⬅️ URLs start with /static
    template_folder=os.path.join(BASE_DIR, 'src/pages')    # ⬅️ HTML lives here
)

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

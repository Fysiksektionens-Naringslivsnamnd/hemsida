import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

__version__ = "1.0.0"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

load_dotenv()

ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PW_HASH")

if not ADMIN_PASSWORD_HASH:
    raise ValueError("ADMIN_PW_HASH environment variable is not set.")


app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "src/static"),
    static_url_path="/static",
    template_folder=os.path.join(BASE_DIR, "src/pages"),
)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.config["UPLOAD_FOLDER"] = "src/static/uploads"

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

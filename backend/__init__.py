import os
from flask import Flask
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'static'),        # ⬅️ points to /static
    static_url_path='/static',                             # ⬅️ URLs start with /static
    template_folder=os.path.join(BASE_DIR, 'src/pages')    # ⬅️ HTML lives here
)

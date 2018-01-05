from flask import Flask
import d2lvalence.auth as d2lauth
from conf_basic import app_config, UPLOAD_FOLDER, SECRET_KEY

app = Flask(__name__)


app.config['SECRET_KEY']    = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER#should be moved to config file
app.config["app_context"]   = d2lauth.fashion_app_context(app_id=app_config['app_id'], app_key=app_config['app_key'])

#Strip extra whitespace
app.jinja_env.trim_blocks  = True
app.jinja_env.lstrip_blocks = True


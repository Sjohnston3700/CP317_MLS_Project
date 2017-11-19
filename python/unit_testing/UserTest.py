import d2lvalence.auth as d2lauth
from threading import Thread, Event
import logging
import unittest
from flask import Flask, redirect, request

import os, sys
root_path = os.path.abspath(os.path.join('..'))
obj_path = os.path.abspath(os.path.join('..', 'wrapper', 'obj'))
sys.path.append(root_path)
sys.path.append(obj_path)

from conf_basic import app_config
from Host import Host
from OrgMember import User

LOGOUT_URL = 'https://{host}/d2l/logout'

app = Flask(__name__)
app.config["app_context"] = d2lauth.fashion_app_context(app_id=app_config['app_id'], app_key=app_config['app_key'])

app_url = '{0}://{1}:{2}{3}'.format(app_config['scheme'], app_config['host'], app_config['port'], app_config["route"])

@app.route("/")
def start():
    aurl = app.config["app_context"].create_url_for_authentication(app_config["lms_host"], app_url)
    return redirect(aurl)

@app.route(app_config["route"])
def auth_token_handler():
    print("Authentication successful.")
    
    uc = app.config["app_context"].create_user_context(result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])
    host = Host(app_config['lms_host'])
    # store the user context's
    user = User(uc, host)
    app.config['user'] = user
    
    print("Starting test thread...")
    
    # creates and starts a new thread for the unit tests to run in
    thread = Thread(target=unittest.main, args=())
    thread.start()
    
    # waits for the testing to finish
    thread.join()
    
    sys.exit(0)    

# unit testing class
# do not change setUp and tearDown to snake case, it'll break
class test_user(unittest.TestCase):
    # stores the user object before every test
    def setUp(self):
        self.user = app.config['user']

    # prints the user's name
    def test_who_am_i(self):
        print(self.user.get_name())
    
    def tearDown(self):
        return

# says that if running this file, call unittest.main (which calls setUp)    
if __name__ == "__main__":
    # gets rid of Flask's HTTP request logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    print("Go to {0}://{1}:{2} to authenticate.".format(app_config['scheme'], app_config['host'], app_config['port']))
    app.run(port=8080,debug=False)
"""
Tests User class
Requires that Host, API file work
start() and auth_token_handler() needed to get user context

Click the url that appears in the console, fill in user credentials
Can debug in Web debugger, just go to last couple lines to see what caused error
and then can click terminal icon on right side query for object data

Nothing will work until various bugs get fixed. I (Troy) have fixed some already, but stopping because not my role

Version: Nov. 16, 2017
"""


import unittest # need, even though says import not used
from OrgMember import User
import requests # may not need. Delete if so
import d2lvalence.auth as d2lauth

from flask import Flask, redirect, request
from conf_basic import app_config
from Host import Host

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
    uc = app.config["app_context"].create_user_context( result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])
    host = Host(app_config['lms_host'])
    # store the user context's
    user = User(uc, host)
    app.config['user'] = user

# add tests to this class for user
# need to make it so that messages are displayed for tests
class test_user(unittest.TestCase):

    # runs start(), which then calls auth_token_handler()
    # user object will be stored in app.config after
    # could try changing to set_up to match standard, but not sure if unittest will handle that
    def setUp(self):
        app.run(port=8080,debug=True)

    def test_who_am_i(self):
        print(app.config['user'].get_name())
    
    #should probably put logout here
    def tearDown(self):
        return

# says that if running this file, call unittest.main (which calls setUp)    
if __name__ == "__main__":
    unittest.main()
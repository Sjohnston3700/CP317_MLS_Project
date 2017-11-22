'''
Created on 2017 M11 22

@author: Kosta
get_api_versions unit test
Following GradeTest template
'''
import unittest

from OrgMember import User

import Course
import OrgMember
import d2lvalence.auth as d2lauth
import API

from flask import Flask, redirect, request
from conf_basic import app_config
from Host import Host


app = Flask(__name__)
app.config["app_context"] = d2lauth.fashion_app_context(app_id=app_config['app_id'], app_key=app_config['app_key'])

print("Hi")
app_url = '{0}://{1}:{2}{3}'.format(app_config['scheme'], app_config['host'], app_config['port'], app_config["route"])


@app.route("/")
def start():
    aurl = app.config["app_context"].create_url_for_authentication(app_config["lms_host"], app_url)
    return redirect(aurl)

@app.route(app_config["route"])
def auth_token_handler():
    uc = app.config["app_context"].create_user_context(result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])
    host = Host(app_config['lms_host'])
    # store the user context's
    user = User(uc, host)
    app.config['user'] = user
    
    
class test(unittest.TestCase):
    def setUp(self):
        host = Host(app_config['lms_host'])
        results = API.get_api_versions(host)
        print(results)
        app.run(port=8080,debug=True)
        
    def test_get_value(self):
        #print(numeric_grade.get_value())
        print("Put grade and is now: ", app.config['user'].get_value())
        
    

#says that if running this file, call unittest.main (which calls setUp)    
if __name__ == "__main__":
    unittest.main()
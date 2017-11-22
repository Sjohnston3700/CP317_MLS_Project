"""
Tests Grade class which also contains Numeric Grade class

Click the url that appears in the console, fill in user credentials
Can debug in Web debugger, just go to last couple lines to see what caused error
and then can click terminal icon on right side query for object data

Version: Nov. 18, 2017
"""

# import d2lvalence.auth as d2lauth
# from threading import Thread, Event
# import logging
# from flask import Flask, redirect, request
import unittest

import os, sys

"""
Needed to access files not in the unit testing folder
"""
file_path = os.path.abspath(__file__)
root_path = os.path.abspath(os.path.join(file_path, "..", ".."))
obj_path = os.path.realpath(os.path.join(file_path, "..", "..", 'wrapper', 'obj'))
sys.path.append(os.path.abspath(root_path))
sys.path.append(os.path.abspath(obj_path))

import Grade
from Grade import NumericGrade
# from conf_basic import app_config
# from Host import Host
# import OrgMember
# from OrgMember import User


# LOGOUT_URL = 'https://{host}/d2l/logout'
#  
# app = Flask(__name__)
# app.config["app_context"] = d2lauth.fashion_app_context(app_id=app_config['app_id'], app_key=app_config['app_key'])
#  
# app_url = '{0}://{1}:{2}{3}'.format(app_config['scheme'], app_config['host'], app_config['port'], app_config["route"])
#  
# """
# start() and auth_token_handler() needed to get user context
# """
# @app.route("/")
# def start():
#     aurl = app.config["app_context"].create_url_for_authentication(app_config["lms_host"], app_url)
#     return redirect(aurl)
#  
# @app.route(app_config["route"])
# def auth_token_handler():
#     print("Authentication successful.")
#      
#     uc = app.config["app_context"].create_user_context(result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])
#     host = Host(app_config['lms_host'])
#      
#     # stores the user context's
#     user = User(uc, host)
#     app.config['user'] = user
#      
#     print("Starting test thread...")
#      
#     # creates and starts a new thread for the unit tests to run in
#     thread = Thread(target=unittest.main, args=())
#     thread.start()
#      
#     # waits for the testing to finish
#     thread.join()
#      
#     sys.exit(0)    

# unit testing class
# do not change setUp and tearDown to snake case, it'll break
class test_user(unittest.TestCase):
    # stores the user object before every test
    def setUp(self):
        self.Grade = app.config['Grade']
        self.NumericGrade = app.config['NumericGrade']

    def test_get_comment(self):
        self.assertEqual(self.Grade.get_comment(), "Nice", "Comment 'Nice' was not retrieved")
        pass
    
    def test_get_grade_item(self):
        self.assertIsInstance(self.Grade.get_grade_item(), GradeItem, "GradeItem object was not found")
        pass
        
    def test_get_student(self):
        self.assertIsInstance(self.Grade.get_student(), OrgMember, "Student (OrgMember) object was not found")
        pass
        
    def test_get_user(self):
        self.assertIsInstance(self.Grade.get_user(), User, "User object was not found")
        pass
        
    def test_put_grade(self):
        grade = self.Grade.put_grade()
        self.assertEqual(self.NumericGrade.get_value(), 0, "Grade '0' was not retrieved")
        pass

    def test_get_value(self):
        self.assertEqual(self.NumericGrade.get_value(), 100, "Grade '100' was not retrieved")
        pass
    
    def tearDown(self):
        return

# says that if running this file, call unittest.main (which calls setUp)    
if __name__ == "__main__":
#     # gets rid of Flask's HTTP request logging
#     log = logging.getLogger('werkzeug')
#     log.setLevel(logging.ERROR)
#      
#     print("Go to {0}://{1}:{2} to authenticate.".format(app_config['scheme'], app_config['host'], app_config['port']))
#     app.run(port=8080,debug=True)
    unittest.main()
"""
Tests Grade class which also contains Numeric Grade class
start() and auth_token_handler() needed to get user context

Click the url that appears in the console, fill in user credentials
Can debug in Web debugger, just go to last couple lines to see what caused error
and then can click terminal icon on right side query for object data

Unknown if working right now. Still trying to get it to work. - Simon Phothitay

Version: Nov. 18, 2017
"""

import unittest # need, even though says import not used

from Orgmember import User
# import Course
# import GradeItem
# import OrgMember
# import Grade

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

# need to make it so that messages are displayed for tests
class test_user(unittest.TestCase):
#     grade = None
#     numeric_grade = None
    # runs start(), which then calls auth_token_handler()
    # user object will be stored in app.config after
    # could try changing to set_up to match standard, but not sure if unittest will handle that
    def setUp(self):
#         uc = app.config["app_context"].create_user_context( result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])
#         host = Host(app_config['lms_host'])
#         user = User(uc, host)
#         course_params = {'OrgUnit': 'John Smith', 'OrgUnit': 150000000, 'Access': 'Unknown'}
#         course = Course(user, course_params)
#         grade_item_params = {'Name': 'John Smith', 'Id': 150000000}
#         grade_item = GradeItem(course, grade_item_params)
#         
#         org_member_params = {'User': 150000000, 'User': 'JohnSmith', 'User': None, 'Role': None}
#         student = OrgMember(org_member_params)
#         
#         comment = "Nice"
#         
#         grade = Grade(grade_item, student, comment)
#         
#         value = 100
#         numeric_grade = NumericGrade(grade_item, student, comment, value)
        
        app.run(port=8080,debug=True)

    def test_get_comment(self):
        #print(grade.get_name())
        print(app.config['user'].get_comment())
        
    def test_get_grade_item(self):
        #print(grade.get_grade_item())
        print(app.config['user'].get_grade_item())
        
    def test_get_student(self):
        #print(grade.get_student())
        print(app.config['user'].get_student())
        
    def test_get_user(self):
        #print(grade.get_user().get_user())
        print(app.config['user'].get_user())
        
    def test_put_grade(self):
        #grade.put_grade()
        #print("Put grade and is now: ", grade.get_grade_item)
        app.config['user'].put_grade()
        print("Put grade and is now: ", app.config['user'].get_grade_item())

    def test_get_value(self):
        #print(numeric_grade.get_value())
        print("Put grade and is now: ", app.config['user'].get_value())
        
    #should probably put logout here
    def tearDown(self):
        return

# says that if running this file, call unittest.main (which calls setUp)    
if __name__ == "__main__":
    unittest.main()
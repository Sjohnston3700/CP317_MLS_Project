import d2lvalence.auth as d2lauth
from threading import Thread, Event
import logging
import unittest
from flask import Flask, redirect, request
import os, sys
file_path = os.path.abspath(__file__)
root_path = os.path.abspath(os.path.join(file_path, "..", ".."))
obj_path = os.path.realpath(os.path.join(file_path, "..", "..", 'wrapper', 'obj'))
sys.path.append(os.path.abspath(root_path))
sys.path.append(os.path.abspath(obj_path))
from wrapper.obj.OrgMember import User
from wrapper.obj.User import User
from wrapper.obj.Host import Host
from conf_basic import app_config
import Course 
from wrapper.obj.User import User
import Grade
from Grade import NumericGrade
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
    user=User(uc,host,[])
    
    
    app.config['user'] = user
    
    print("Starting test thread...")
    
    # creates and starts a new thread for the unit tests to run in
    thread = Thread(target=unittest.main, args=())
    thread.start()
    
    # waits for the testing to finish
    thread.join()
    
    return "ok"

# unit testing class
# do not change setUp and tearDown to snake case, it'll break
class test_user(unittest.TestCase):
    # stores the user object before every test
    def setUp(self):
        self.user = app.config['user']
        self.course = self.user.get_course(219318) # gets test course
    # prints list of grade itmes
    def test_get_grade_items(self):
        print('get_grade_items test'+'\n')
        print(self.course.get_grade_items())
        print('\n')
    # prints the specific grade item
    def test_get_grade_item(self):
        print('get_grade_item test'+'\n')
        gradei = self.course.get_grade_item(223607)
        print(gradei)
        print('\n')
    # prints the course ID
    def test_get_id(self):
        print('get_id test'+'\n')
        print(self.course.get_id)
        print('\n')
    # prints the course Name
    def test_get_name(self):
        print('get_name test'+'\n')
        print(self.course.get_name())
        print('\n')
    # prints the list of members in the course
    def test_get_members(self):
        print('get_members test'+'\n')
        print(self.course.get_members())
        print('\n')
    # prints the specific member in the course, prints none if member not found
    def test_get_member(self):
        print('get_member test'+'\n')
        print(self.course.get_member(123))
        print('\n')
    # prints the users name
    def test_get_user(self):
        print('get_user test'+'\n')
        print(self.course.get_user().get_name())
        print('\n')
    # prints the users role
    def test_get_user_role(self):
        print('get_user_role test'+'\n')
        print(self.course.get_user_role())    
        print('\n')
    def tearDown(self):
        return

# says that if running this file, call unittest.main (which calls setUp)    
if __name__ == "__main__":
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    print("Go to {0}://{1}:{2} to authenticate.".format(app_config['scheme'], app_config['host'], app_config['port']))
    app.run(port=8080,debug=True)
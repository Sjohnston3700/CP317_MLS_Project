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

from conf_basic import app_config
from Host import Host
from OrgMember import User
from Course import Course
from GradeItem import GradeItem
from GradeItem import NumericGradeItem

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
    
    return "ok"

# unit testing class
# do not change setUp and tearDown to snake case, it'll break
class TestGradeItem(unittest.TestCase):
    def setUp(self):
        self.user = app.config['user']
        self.course = self.user.get_course(219318) # gets test course
        self.grade_item_1 = self.course.get_grade_item(223607) # gets A1 Can NOT exceed
        self.grade_item_2 = self.course.get_grade_item(223608) # gets A2 Can exceed
        pass

    def test_init_grade_item(self):
        with self.assertRaises(TypeError):
            GradeItem(None, None) # params irrelevant, should raise TypeError before getting params
        pass
    
    def test_can_exceed(self):
        self.assertFalse(self.grade_item_1.can_exceed(), "Can exceed should be False for A1, not True")
        pass

    def test_can_not_exceed(self):
        self.assertTrue(self.grade_item_2.can_exceed(), "Can exceed should be True for A2, not False")
        pass

    def test_get_max(self):
        self.assertEqual(self.grade_item_1.get_max(), 34, "Maximum grade should be 34 for A1")
        pass

    def test_within_max(self):
        self.assertTrue(self.grade_item_1.within_max(33), "33 should be within maximum of 34 for A1")
        pass

    def test_not_within_max(self):
        self.assertFalse(self.grade_item_1.within_max(35), "35 should not be within maximum of 34 for A1")
        pass

    def test_get_course(self):
        self.assertIsInstance(self.grade_item_1.get_course(), Course, "Not an instance of Course")
        pass

    def test_get_id(self):
        self.assertEqual(self.grade_item_1.get_id(), 223607, "A1 ID isn't 223607")
        pass
    
    def test_get_name(self):
        self.assertEqual(self.grade_item_1.get_name(), "A1 Can NOT exceed", "Name for A1 should be \"A1 Can NOT exceed\"")
        pass

    def test_get_user(self):
        self.assertIsInstance(self.grade_item_1.get_user(), User, "Not an instance of User")
        pass

    """
    @TODO Create the following tests: 
            - test_create_grade
            - test_get_grade
            - test_get_grades
            - test_put_grade_item
            - test_put_grades
    """

    def tearDown(self):
        pass

# says that if running this file, call unittest.main (which calls setUp)    
if __name__ == "__main__":
    # gets rid of Flask's HTTP request logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    print("Go to {0}://{1}:{2} to authenticate.".format(app_config['scheme'], app_config['host'], app_config['port']))
    app.run(port=8080,debug=True)
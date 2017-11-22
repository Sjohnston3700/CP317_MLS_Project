'''
Created on 2017 M11 20

@author: Andrew Chua 150693280
'''

import unittest
from OrgMember import OrgMember
import Host
from OrgMember import User
from flask import Flask, redirect, request
from conf_basic import app_config
import d2lvalence.auth as d2lauth

class test():
#    app = Flask(__name__)
#    app.config["app_context"] = d2lauth.fashion_app_context(app_id=app_config['app_id'], app_key=app_config['app_key'])
#    app_url = '{0}://{1}:{2}{3}'.format(app_config['scheme'], app_config['host'], app_config['port'], app_config["route"])

#    uc = app.config["app_context"].create_user_context( result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])
#    host = Host(app_config['lms_host'])
#    user = User(uc, host)
    
    org_member_params = {'User':{'Identifier': 150123456, 'DisplayName': 'Andrew Chua', 'OrgDefinedId': 22}, 
                        'Role': {'Id':None}}
    student = OrgMember(org_member_params)
    
    print(student.get_id())
    print(student.get_name())
    print(student.get_org_id())
    print(student.get_role())
    
#    Currently testing only OrgMember, User functions still to come.
    
#if __name__ == "__main__":
#    unittest.main()
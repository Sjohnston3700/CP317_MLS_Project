'''
Functions that interact with the frontend via AJAX requests.
'''
import os, logging
from app import app
from flask import json, session, request, abort
from werkzeug.utils import secure_filename
from conf_basic import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

from wrapper.obj import API
from wrapper.obj.User import User
from wrapper.obj.Host import Host
from grade_functions import *
from grade_item_functions import *



logger = logging.getLogger(__name__)

def allowed_file(filename):
    '''
    Helper function to file_parse(); Determines if file extension is valid.
    Preconditions:
        filename (string) : name of file in question.
    Postconditions:
        boolean : True if file is valid, False if not.
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/actions/get_courses.py',methods=['POST'])
def get_courses():
    '''
    Function to handle ajax requests for courses.
    Postconditions:
        On success:
            If user_id in session : Returns json list of courses and gradeitems
        On failure:
            aborts with a 403 if not logged in, aborts with 404 if anything else goes wrong.
    '''
    try:
        if 'user_id' not in session or app.config.get( session.get('user_id',None), None) is None:
            abort(403)
        else:
            courses = []
            user = app.config.get( session.get('user_id',None), None)
            for course in user.get_courses():
                data = {}
                data['name'] = course.get_name()
                data['id']   = course.get_id()
                
                data['grade_items'] = []
                for grade_item in course.get_grade_items():
                    data['grade_items'].append( {'name':grade_item.get_name(), 'id':grade_item.get_id()} ) 
                courses.append(data)
            
            #Sort courses by name before returning them   
            courses.sort(key = lambda x: x['name'] )    
            return json.dumps(courses)
    except Exception as e:
        logger.error('Something went wrong in /actions/get_courses.py : {}'.format(e) )
        abort(404)
    
    

@app.route('/actions/file_parse.py',methods=['POST'])
def file_parse():
    '''
    Function to accept uploaded file and parse it for errors.
    Preconditions:
        file (file) : File sent through request.files.
    Postconditions:
        Returns JSON list of errors or grade items
        On success:
            JSON list of grade items
        On failure:
            JSON list of errors
    '''
        
    user = app.config[session['user_id']]   
    
    errors = []
    # check if the post request has the file part
    if 'file' not in request.files:
        logger.error('No file part in request to /file_parse')
        errors = [{'msg':'No file part in request'}]
    else:
        file = request.files['file']
        
        if file.filename == '':
            logger.error('No selected file in /file_parse')
            errors = [{'msg':'No file selected'}]
        elif file and allowed_file(file.filename):
            filename = user.get_id() + secure_filename(file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            file.save( full_path )
            
            #parse file in memory
            results=[]
            with open(full_path,'r') as f:
                results = parse_grades(f)
            os.remove(full_path)  
            if len(errors) == 0:                 
                return json.dumps(results)
            else:
                return json.dumps(errors)
        elif not allowed_file(file.filename):
            errors = [{'msg':'Incorrect file type. Must be .csv or .txt'}] 
    return json.dumps(errors)


@app.route('/actions/error_checking.py',methods=['POST'])
def grades_error_checking():
    '''
    Checks grades submitted from form.
    Preconditions:
        grades_json (dict) : json information for each grade being checked.
    Postconditions:
        returns json.dump(errors) (str) : success/errors messages for grades.
    '''
    
    grades_json  = request.get_json(force=True)
    grades       = grades_json['grades']
    course_id    = grades_json['courseId']
    grade_item_id = grades_json['gradeItemId']
    
    user       = app.config[ session['user_id' ] ]
    course     = user.get_course(course_id)
    grade_item = course.get_grade_item(grade_item_id)
    
    errors, valid_grades = check_grades(grades, grade_item)
    
    
    '''
    if len(errors) == 0:
        successful_grades, failed_grades = API.put_grades(valid_grades)
        report = {'successful_grades':successful_grades, 'failed_grades':failed_grades}
        
        key = '{}_report'.format(user.get_id() )
        app.config[key] = report
    '''
    return json.dumps(errors)

@app.route('/actions/update_max.py',methods=['POST'])
def update_grade_max():
    '''
    Function to receive update grade max requests and try to execute them.
    Preconditions:
        new_max (string)     : New grade maximum, obtained through request.form.
        courseId (string)    : Course Id, obtained through request.form.
        gradeItemId (string) : GradeItem Id, obtained through request.form.
    Postconditions:
        returns JSON list of errors [] if none
    '''
    new_max       = request.form['new_max']
    course_id     = request.form['courseId']
    grade_item_id = request.form['gradeItemId']

     
    user = app.config[session['user_id']]
    course = user.get_course(course_id)
    grade_item = course.get_grade_item(grade_item_id)

    errors = modify_grade_max(grade_item, new_max)
    
    return json.dumps(errors)
    
@app.route('/actions/upload_grades.py',methods=['POST'])
def upload_grades():
    '''
    Function to upload grades to Brightspace
    Preconditions:
        grades_json (dict)   : json information for each grade being checked.
        courseId (string)    : Course Id, obtained through request.form.
        gradeItemId (string) : GradeItem Id, obtained through request.form.
    Postconditions:
        returns json.dump(errors) (str) : success/errors messages for grade upload.    
    '''
    grades_json  = request.get_json(force=True)
    if 'grades' not in grades_json:
        return json.dumps({'error':"You didn't submit any grades"})

    grades        = grades_json['grades']
    course_id     = grades_json['courseId']
    grade_item_id = grades_json['gradeItemId']
     
    user = app.config[session['user_id']]
    course = user.get_course(course_id)
    grade_item = course.get_grade_item(grade_item_id)
    
    errors = upload_grades_function(grades, user, course, grade_item)
    
    return json.dumps(errors)
    
        


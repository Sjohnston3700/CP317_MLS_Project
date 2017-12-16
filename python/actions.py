'''
Functions that interact with the frontend via AJAX requests.
'''
import os
from app import app
from flask import json, session, request
from werkzeug.utils import secure_filename

from wrapper.obj import API
from wrapper.obj.User import User
from wrapper.obj.Host import Host
from grade_functions import parse_grades, check_grades
from grade_item_functions import *



ALLOWED_EXTENSIONS = set(['txt','dat','csv'])
UPLOAD_FOLDER = './Uploaded_Files'

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
            aborts with a 403 response.
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
            return json.dumps(courses)
    except:
        abort(404)
    
    

@app.route('/actions/file_parse.py',methods=['POST'])
def file_parse():
    '''
    Function to accept uploaded file and parse it for errors.
    Preconditions:
        file (file) : File sent through request.files.
    Postconditions:
        On success:
            JSON dump of results
        On failure:
            JSON dump of errors
    '''
    if 'user_id' not in session:
        logger.warning('Someone is trying to upload a file but is not logged in')
        return redirect('/login')
    elif app.config.get( session['user_id'] , None) is None:
        logger.warning('Session is out of sync on /file_parse')
        return redirect('/login')
        
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
            with open(full_path,'r') as f:
                results = parse_grades(f)    
                if len(errors) == 0:
                    return json.dumps(results)
  
            os.remove(full_path)

    return json.dumps(errors)

@app.route('/actions/error_checking.py',methods=['POST'])
def grades_error_checking():
    '''
    Checks grades submitted from form.
    Preconditions:
        grades_json (dict) : json information for each grade being checked.
    Postconditions:
        if error with User:
            returns redirect to "/login"
        else:
            returns json.dump(errors) (str) : success/errors messages for grades.
    '''
    if 'user_id' not in session:
        logger.warning('Someone is trying to error check grades but is not logged in')
        return redirect('/login')
    elif app.config.get( session['user_id'] , None) is None:
        logger.warning('Session is out of sync on /error_checking')
        return redirect('/login')
        
    grades_json  = request.get_json(force=True)
    grades       = grades_json['grades']
    course_id    = grades_json['courseId']
    grade_item_id = grades_json['gradeItemId']
    
    user       = app.config[ session['user_id' ] ]
    course     = user.get_course(course_id)
    grade_item = course.get_grade_item(grade_item_id)
    
    errors, valid_grades = check_grades(grades, grade_item)
    if len(errors) == 0:
        successful_grades, failed_grades = API.put_grades(valid_grades)
        report = {'successful_grades':successful_grades, 'failed_grades':failed_grades}
        
        key = '{}_report'.format(user.get_id() )
        app.config[key] = report
    
    return json.dumps(errors)




@app.route('/actions/update_max.py',methods=['POST'])
def update_grade_max():
    '''
    Function to receive update grade max requests and try to execute them.
    Preconditions:
        new_max (string) : New grade maximum, obtained through request.form.
        courseId (string) : Course Id, obtained through request.form.
        gradeItemId (string) : GradeItem Id, obtained through request.form.
    Postconditions:
        On success:
            If 'user_id' in session:
                JSON of any errors (if any).
            Else:
                Redirects to "/login/".
        On failure:
            Renders "error.html".
    '''
    new_max       = request.form['new_max']
    course_id     = request.form['courseId']
    grade_item_id = request.form['gradeItemId']

     
    user = app.config[session['user_id']]
    course = user.get_course(course_id)
    grade_item = course.get_grade_item(grade_item_id)

    errors = modify_grade_max(grade_item, new_max)
    
    return json.dumps(errors)

    
        


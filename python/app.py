import os, sys, requests, traceback
import d2lvalence.auth as d2lauth
import logging, logging.config


from flask import Flask, redirect, request, render_template, url_for, session, jsonify, json
from werkzeug.utils import secure_filename
from conf_basic import app_config
from wrapper.obj import API

from wrapper.obj.User import User
from wrapper.obj.Host import Host
from grade_functions import parse_grades_csv

#Setup logging - Should be moved to a separate function ultimately
logger = logging.getLogger(__name__)
with open('logging_config.json', 'rt') as f:
    config = json.load(f)
    logging.config.dictConfig(config)



EDIT_GRADE_ITEM_URL = 'https://{host}/d2l/lms/grades/admin/manage/item_props_newedit.d2l?objectId={gradeItemId}&gradesArea=1&ou={courseId}'
VIEW_GRADES_URL     = 'https://{host}/d2l/lms/grades/admin/enter/grade_item_edit.d2l?objectId={gradeItemId}&ou={courseId}'
LOGOUT_URL          = 'https://{host}/d2l/logout'


UPLOAD_FOLDER = './Uploaded_Files'
ALLOWED_EXTENSIONS = set(['txt','dat','csv'])


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER#should be moved to config file
app.config["app_context"] = d2lauth.fashion_app_context(app_id=app_config['app_id'], app_key=app_config['app_key'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app_url = '{0}://{1}:{2}{3}'.format(app_config['scheme'], app_config['host'], app_config['port'], app_config["route"])
host = Host(app_config['lms_host'], versions=app_config['lms_ver'])

@app.route("/")
def start():
    return redirect('/login')

@app.route("/login/")
def login():
    aurl = app.config["app_context"].create_url_for_authentication(app_config["lms_host"], app_url)
    return redirect(aurl)

@app.route(app_config["route"])
def auth_token_handler():
    try:
        uc = app.config["app_context"].create_user_context( result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])
        # store the user context's
        user = User(uc, host,['TA','Instructor'])
        user_id = user.get_id()
        session['user_id'] = user_id
        app.config[user_id] = user
        return redirect('/courses/')
    except Exception as e:
        return render_template('error.html',user=None,error=traceback.format_exc())

@app.route('/courses/')
def show_courses():
    if 'user_id' not in session:
        logger.warning('Someone tried to access /courses/ without logging in')
        return redirect('/login')
    else:
        try:
            return render_template('available_grades.html', user=app.config[ session['user_id'] ] )
        except Exception as e :
            logger.exception( "Something went wrong in /courses/" )
            return render_template('error.html',user=app.config[ session['user_id'] ],error=traceback.format_exc())

@app.route('/documentation/')
def show_docs():
    return render_template('documentation.html')

@app.route('/documentation/spmp/')
def show_spmp():
    return render_template('spmp.html')

@app.route('/documentation/requirements')
def show_requirements():
    return render_template('requirements.html')

@app.route('/documentation/requirements/wrapper')
def show_requirements_wrapper():
    return render_template('requirements_wrapper.html')

@app.route('/documentation/analysis')
def show_analysis():
    return render_template('analysis.html')

@app.route('/documentation/analysis/wrapper')
def show_analysis_wrapper():
    return render_template('analysis_wrapper.html')

@app.route('/documentation/design')
def show_design():
    return render_template('design.html')

@app.route('/documentation/design/wrapper')
def show_design_wrapper():
    return render_template('design_wrapper.html')

@app.errorhandler(Exception)
def handle_error(e):
    '''
    Default error handler. If something goes wrong in a route this gets called.
    '''
    if 'user_id' not in session:
        user = None
    else:
        user = app.config[ session['user_id'] ]
    return render_template('error.html',user=user,error=traceback.format_exc())
    
    
@app.route('/upload', methods = ['GET'])
def show_upload():
    """
    Here goes something
    """
    
    
    if 'user_id' not in session:
        logger.warning('Someone tried to access /upload without logging in')
        return redirect('/login')
    
    courseId    = request.args.get('courseId',    default = None, type = int)
    gradeItemId = request.args.get('gradeItemId', default = None, type = int)
    
    try:
        user = app.config[session['user_id']]
        course = user.get_course(courseId)
        grade_item = course.get_grade_item(gradeItemId)
    except Exception as e:
        logger.exception("Something went wrong in {}".format(request.get_url() ))
        return render_template('error.html',user=app.config[ session['user_id'] ],error=traceback.format_exc())
    
    if request.method == "GET":
       return render_template('upload.html',user=user,course=course,grade_item=grade_item)
    else:#It must have been a post
        if request.is_xhr or request.accept_mimetypes.accept_json:#It might have been AJAX
            print("We were sent json")#place holder. Need to figure out what was posted        
            return jsonify(43)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file_parse',methods=['POST'])
def file_parse():
    '''
    Function to accept uploaded file and parse it for errors
    '''
    if 'user_id' not in session:
        logger.warning('Someone is trying to upload a file but is not logged in')
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
                results = parse_grades_csv(f)    
                if len(errors) == 0:
                    return json.dumps(results)
            
            os.remove(full_path)
                    
    return json.dumps(errors)

@app.route('/update_gradeItem_max',methods=['POST'])
def update_grade_max():
    '''
    Function to receive update grade max requests and try to execute them
    '''
    if 'user_id' not in session:
        logger.warning('Someone tried to access /update_gradeItem_max without logging in')
        return redirect('/login')
    
    try:
        print("Extracting")
        new_max     = request.form['new_max']
        courseId    = request.form['courseId']
        gradeItemId = request.form['gradeItemId']
        print("{} {} {}".format(new_max,courseId,gradeItemId) )
         
        user = app.config[session['user_id']]
        course = user.get_course(courseId)
        grade_item = course.get_grade_item(gradeItemId)
        
        print("checking")
        errors = modify_grade_max(grade_item, new_max)
        return jsonify(errors)
        
    except Exception as e:
        logger.exception("Something went wrong in update_gradeItem_max")
        return render_template('error.html',user=app.config[ session['user_id'] ],error=traceback.format_exc())
    
        

def modify_grade_max(grade_item, new_max):
    '''
    Function to try and update grade max
    '''
    
    errors = []
    if new_max is None:
        errors.append({'msg':'Missing new grade item maximum'})
    else:
        try:
            new_max = float(new_max)
        except:
            errors.append({'msg':'Grade maximum must be a number'})
            return errors
            
        if new_max < 0:
            errors.append({'msg':'Grade maximum must be a non-negative number'})
        else:
            try:
                grade_item.set_max( new_max )
            except Exception as e:
                errors.append({'msg':str(e)})
    return errors
        
@app.route('/logout/')
def show_logout():
    if 'user_id' in session:
        app.config.pop( session['user_id'] )
        session.clear()
        return redirect(LOGOUT_URL.format(host=app_config['lms_host']))
    else:
        logger.warning('Someone tried to logout without having logged in')
        return redirect('/login')
                

def set_grades(courseId, gradeItemId):
    try:
        user=app.config[ session['user_id'] ]
        course = user.get_course(courseId)
        grade_item = course.get_grade_item(gradeItemId)
    except Exception as e:
        logger.exception("Something went wrong in /grades/{}/{}/".format(courseId,gradeItemId) )
        return render_template('error.html',user=app.config[ session['user_id'] ],error=traceback.format_exc())
        
    f = request.files['file']
    grades = parse_grades( f.read().decode("utf-8") )
        
    errors = []
    successful_grades = 0
    for grade in grades:
        try:
            if float(grade.maxValue) != grade_item.maxPoints:
                updateUrl = EDIT_GRADE_ITEM_URL.format(host=user.uc.host,gradeItemId=grade_item.get_id(),courseId=course.get_id())
                message = 'Grade for {} is out of {}. The Max Points for {} is {}'.format(grade.studentName,grade.maxValue,grade_item.name,grade_item.maxPoints)
                #return render_template("update_grade_item.html",gradeUrl=updateUrl,message=message)
            
            userId,gradeValue,PublicFeedback = grade.userId,grade.value,grade.public_feedback
            gradeItem.setUserGrade(userId,courseId,gradeValue,PublicFeedback,PrivateFeedback='')
            successful_grades += 1
        
        except RuntimeError as e:
            error = str(e)
            errors.append(error)             
            continue
            
        except AssertionError as e:
            error = '{} for {}'.format(e,grade.studentName)
            errors.append( error )
            continue
    
    gradesUrl = VIEW_GRADES_URL.format(host=user.get_host().get_lms_host(),gradeItemId=grade_item.Id,courseId=course.Id)
    logoutUrl = LOGOUT_URL.format(host=user.get_host().get_lms_host())
    return render_template("grades_uploaded.html",user=user,errors=errors,successful_grades=successful_grades,grades=grades,course=course,gradeItem=grade_item,gradesUrl=gradesUrl,logoutUrl=logoutUrl)
'''
def modify_grade_max(course_id, grade_item_id):
    """
        Update maximum grade points for the grade_item and put
        Precondition:
            grade_item_id - unique id for the grade item
            course_id - unique id for the course
            max - maximum points to be changed to (obtain from request)
        Postcondition:
            Edit this grade item's maximum total grade
    """
    max = int(request.form['max'])
    
    if max >= 0.01 and max <= 9999999999: # MaxPoints for grade item needs to be within this range (indicated by API)
        user = app.config[session['user_id']]
        course = user.get_course(course_id)
        grade_item = course.get_grade_item(grade_item_id)
        grade_item.set_max(max)
        return render_template('upload.html',user=user,course=course,grade_item=grade_item)
    else:
        raise RuntimeError("Max grade need to be greater than 0")
'''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host=app_config['host'], port=port, debug=app_config["debug"])

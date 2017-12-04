import os, sys, requests, traceback
import d2lvalence.auth as d2lauth
import logging, logging.config


from flask import Flask, redirect, request, render_template, url_for, session, jsonify, json
from werkzeug.utils import secure_filename
from conf_basic import app_config
from wrapper.obj import API

from wrapper.obj.User import User
from wrapper.obj.Host import Host
from grade_functions import parse_grades_csv, check_grades

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
    '''
    Function runs at "/" URL, redirects to login.
    Postconditions:
        Redirect user to "/login/".
    '''
    return redirect('/login/')

@app.route("/login/")
def login():
    '''
    Function redirects user to Brightspace secure login page to authenticate user.
    Postconditions:
        Redirect to Brightspace login page.
    '''
    aurl = app.config["app_context"].create_url_for_authentication(app_config["lms_host"], app_url)
    return redirect(aurl)

@app.route(app_config["route"])
def auth_token_handler():
    '''
    Authenticaion token handler - Creates User and user context.
    Postcontitions:
        On success:
            Redirect to "/courses/".
        On failure:
            Renders "error.html".  
    '''
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
    '''
    Runs when application pointed to "/courses/" URL.
    Postconditions:
        On success:
            If user_id in session : Renders "available_grades.html".
            Else : Redirects to "/login/".
        On failure:
            Renders "error.html".
    '''
    if 'user_id' not in session:
        logger.warning('Someone tried to access /courses/ without logging in')
        return redirect('/login/')
    elif app.config.get( session['user_id'] , None) is None:
        logger.warning('Session is out of sync on /courses')
        return redirect('/login')
    else:
        try:
            return render_template('available_grades.html', user=app.config[ session['user_id'] ] )
        except Exception as e :
            logger.exception( "Something went wrong in /courses/" )
            return render_template('error.html',user=app.config[ session['user_id'] ],error=traceback.format_exc())

@app.route('/documentation/')
def show_docs():
    '''
    Runs when application is pointed to "/documentation/".
    Postconditions:
        Renders "documentation.html".
    '''
    return render_template('documentation.html')

@app.route('/documentation/spmp/')
def show_spmp():
    '''
    Runs when application is pointed to "/documentation/spmp/".
    Postconditions:
        Renders "spmp.html".
    '''
    return render_template('spmp.html')

@app.route('/documentation/requirements')
def show_requirements():
    '''
    Runs when application is pointed to "/documentation/requirements/".
    Postconditions:
        Renders "requirements.html".
    '''
    return render_template('requirements.html')

@app.route('/documentation/requirements/wrapper/')
def show_requirements_wrapper():
    '''
    Runs when application is pointed to "/documentation/requirements/wrapper/".
    Postconditions:
        Renders "requirements_wrapper.html".
    '''
    return render_template('requirements_wrapper.html')

@app.route('/documentation/analysis/')
def show_analysis():
    '''
    Runs when application is pointed to "/documentation/analysis/".
    Postconditions:
        Renders "analysis.html".
    '''
    return render_template('analysis.html')

@app.route('/documentation/analysis/wrapper/')
def show_analysis_wrapper():
    '''
    Runs when application is pointed to "/documentation/analysis/wrapper/".
    Postconditions:
        Renders "analysis_wrapper.html".
    '''
    return render_template('analysis_wrapper.html')

@app.route('/documentation/design/')
def show_design():
    '''
    Runs when application is pointed to "/documentation/design/".
    Postconditions:
        Renders "design.html".
    '''
    return render_template('design.html')

@app.route('/documentation/design/wrapper/')
def show_design_wrapper():
    '''
    Runs when application is pointed to "/documentation/spmp/".
    Postconditions:
        Renders "design_wrapper.html".
    '''
    return render_template('design_wrapper.html')

@app.errorhandler(Exception)
def handle_error(e):
    '''
    Default error handler. If something goes wrong in a route this gets called.
    Preconditions:
        e (Exception) : Exception that is being handled.
    Postconditions:
        Renders "error.html".
    '''
    if 'user_id' not in session:
        user = None
    elif app.config.get( session['user_id'] , None) is None:
        logger.warning('Session is out of sync')
        return redirect('/login')
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
    elif app.config.get( session['user_id'] , None) is None:
        logger.warning('Session is out of sync on /upload')
        return redirect('/login')
        
    course_id    = request.args.get('courseId',    default = None, type = int)
    grade_item_id = request.args.get('gradeItemId', default = None, type = int)
    
    try:
        user = app.config[session['user_id']]
        course = user.get_course(course_id)
        grade_item = course.get_grade_item(grade_item_id)
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
    '''
    Helper function to file_parse(); Determines if file extension is valid.
    Preconditions:
        filename (string) : name of file in question.
    Postconditions:
        boolean : True if file is valid, False if not.
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file_parse',methods=['POST'])
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
                results = parse_grades_csv(f)    
                if len(errors) == 0:
                    #I think you want to remove full_path, delete line if not
                    os.remove(full_path)
                    return json.dumps(results)
  
            os.remove(full_path)

    return json.dumps(errors)

@app.route('/error_checking',methods=['POST'])
def grades_error_checking():
    '''
    '''
    if 'user_id' not in session:
        logger.warning('Someone is trying to error check grades but is not logged in')
        return redirect('/login')
    elif app.config.get( session['user_id'] , None) is None:
        logger.warning('Session is out of sync on /error_checking')
        return redirect('/login')
    
    grades_json  = request.get_json()
    grades       = grades_json['grades']
    course_id    = grades_json['courseId']
    grade_item_id = grades_json['gradeItemId']
    
    print("Validing grades = {}".format(grades) )
    user       = app.config[ session['user_id' ] ]
    course     = user.get_course(course_id)
    grade_item = course.get_grade_item(grade_item_id)
    
    
    errors = check_grades(grades, grade_item)
    
    return json.dumps(errors)

@app.route('/report',methods=['GET'])
def report():
    return json.dumps(23)

@app.route('/update_gradeItem_max',methods=['POST'])
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
    if 'user_id' not in session:
        logger.warning('Someone tried to access /update_gradeItem_max without logging in')
        return redirect('/login')
    elif app.config.get( session['user_id'] , None) is None:
        logger.warning('Session is out of sync on /update_gradeItem_return')
        redirect('/login')

    try:
        new_max     = request.form['new_max']
        course_id    = request.form['courseId']
        grade_item_id = request.form['gradeItemId']
        print("{} {} {}".format(new_max,course_id,grade_item_id) )
         
        user = app.config[session['user_id']]
        course = user.get_course(course_id)
        grade_item = course.get_grade_item(grade_item_id)

        errors = modify_grade_max(grade_item, new_max)
        
        return jsonify(errors)
        
    except Exception as e:
        logger.exception("Something went wrong in update_gradeItem_max")
        return render_template('error.html',user=app.config[ session['user_id'] ],error=traceback.format_exc())
    
        

def modify_grade_max(grade_item, new_max):
    '''
    Function to try and update grade max.
    Preconditions:
        grade_item (GradeItem) : GradeItem object to be updated.
        new_max (string) : New maximum grade for the grade_item.
    Postconditions:
        If successful, The GradeItem is updated through the API.
        Returns:
            Errors (list) : Any and all errors that may have occured.
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
                return new_max
            except Exception as e:
                errors.append({'msg':str(e)})
    return errors
        
@app.route('/logout/')
def show_logout():
    '''
    Runs when application pointed to "/logout/" URL.
    Postconditions:
        If user_id in session : redirects user to Brightspace logout page.
        Else : Redirects to "/login/".
    '''
    if 'user_id' in session:
        app.config.pop( session['user_id'] )
        session.clear()
        return redirect(LOGOUT_URL.format(host=app_config['lms_host']))
    else:
        logger.warning('Someone tried to logout without having logged in')
        return redirect('/login/')
                
"""
def set_grades(courseId, gradeItemId):
    '''
    Is this even used anymore? It doesn't work
    '''
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
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host=app_config['host'], port=port, debug=app_config["debug"])

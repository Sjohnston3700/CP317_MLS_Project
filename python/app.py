import os, sys, requests
import d2lvalence.auth as d2lauth

from flask import Flask, redirect, request, render_template, url_for
from werkzeug.utils import secure_filename
from conf_basic import app_config

from User import User
from Host import Host
from grade_functions import parse_grades


EDIT_GRADE_ITEM_URL = 'https://{host}/d2l/lms/grades/admin/manage/item_props_newedit.d2l?objectId={gradeItemId}&gradesArea=1&ou={courseId}'
VIEW_GRADES_URL     = 'https://{host}/d2l/lms/grades/admin/enter/grade_item_edit.d2l?objectId={gradeItemId}&ou={courseId}'
LOGOUT_URL          = 'https://{host}/d2l/logout'

UPLOAD_FOLDER = './Uploaded_Files'
ALLOWED_EXTENSIONS = set(['txt','dat'])


app = Flask(__name__)
app.config["app_context"] = d2lauth.fashion_app_context(app_id=app_config['app_id'], app_key=app_config['app_key'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app_url = '{0}://{1}:{2}{3}'.format(app_config['scheme'], app_config['host'], app_config['port'], app_config["route"])

@app.route("/")
def start():
    return redirect('/login')

@app.route("/login/")
def login():
    aurl = app.config["app_context"].create_url_for_authentication(app_config["lms_host"], app_url)
    return redirect(aurl)

@app.route(app_config["route"])
def auth_token_handler():
    uc = app.config["app_context"].create_user_context( result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])
    host = Host(app_config['lms_host'])
    # store the user context's
    user = User(uc, host)
    app.config['user'] = user
    return redirect('/courses/')

@app.route('/courses/')
def show_courses():
	try:
		return render_template('available_grades.html', user=app.config['user'])
	except:
		return redirect("/")

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

@app.route('/logout/')
def show_logout():
	if 'user' in app.config:
		return redirect(LOGOUT_URL.format(host=app_config['lms_host']))
	else:
		return redirect('/') # TODO maybe logout/general error page? "user not found"

@app.route('/grades/<courseId>/<gradeItemId>', methods = ['GET', 'POST'])
def set_grades(courseId, gradeItemId):
    try:
        user   = app.config['user']
        course = user.get_course(courseId)
        grade_item = course.get_grade_item(gradeItemId)
    except:
        return redirect('/courses/')
    
    if request.method == 'GET':
        return render_template('upload.html',user=user,course=course,grade_item=grade_item)
    
    elif request.method == 'POST':
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

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8080))
	app.run(host='0.0.0.0', port=port, debug=app_config["debug"])

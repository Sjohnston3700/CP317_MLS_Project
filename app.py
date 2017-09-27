import os
from flask import Flask, redirect,request,render_template, url_for
from werkzeug.utils import secure_filename
from conf_basic import app_config
import requests
import d2lvalence.auth as d2lauth
import sys
from User import User
from Grade import parse_grades


EDIT_GRADE_ITEM_URL = 'https://{host}/d2l/lms/grades/admin/manage/item_props_newedit.d2l?objectId={gradeItemId}&gradesArea=1&ou={courseId}'
VIEW_GRADES_URL     = 'https://{host}/d2l/lms/grades/admin/enter/grade_item_edit.d2l?objectId={gradeItemId}&ou={courseId}'
LOGOUT_URL            = 'https://{host}/d2l/logout'

UPLOAD_FOLDER = './Uploaded_Files'
ALLOWED_EXTENSIONS = set(['txt','dat'])


app = Flask(__name__)
app.config["app_context"] = d2lauth.fashion_app_context(app_id=app_config['app_id'], app_key=app_config['app_key'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app_url = 'https://ezmarker.herokuapp.com/token'

@app.route("/")
def start():
	return render_template('home.html')	

@app.route("/login/")
def login():
    aurl = app.config["app_context"].create_url_for_authentication(app_config["lms_host"], app_url)
    return redirect(aurl)

@app.route(app_config["route"])
def auth_token_handler():
    uc = app.config["app_context"].create_user_context( result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])

    # store the user context's
    user = User(uc)
    app.config['user'] = user
    return redirect('/availableCourses/')

@app.route('/availableCourses/')
def showCourses():
	try:
		return render_template('available_grades.html', user=app.config['user'])
	except:
		return redirect("/")

@app.route('/documentation/')
def showDocs():
	return render_template('documentation.html')

@app.route('/documentation/spmp/')
def showSPMP():
	return render_template('spmp.html')

@app.route('/documentation/spmp/raw/')
def showSPMPRaw():
	return render_template('spmp_raw.html')

@app.route('/documentation/requirements')
def showRequirements():
	return render_template('requirements.html')

@app.route('/documentation/requirements/raw/')
def showRequirementsRaw():
	return render_template('requirements_raw.html')

@app.route('/logout/')
def showLogout():
	return render_template(LOGOUT_URL.format(host=user.uc.host))

	

@app.route('/grades/<courseId>/<gradeItemId>', methods = ['GET', 'POST'])
def set_grades(courseId, gradeItemId):
    try:
        user   = app.config['user']
        course = user.getCourse(courseId)
        gradeItem = course.getGradeItem(gradeItemId)
    except:
        return redirect('/availableCourses/')
        
    if request.method == 'GET':
        return render_template('upload.html',courseId=courseId,gradeItemId=gradeItemId)
    
    elif request.method == 'POST':
        f = request.files['file']
        grades = parse_grades( f.read().decode("utf-8") )
        
        errors = []
        successful_grades = 0
        for grade in grades:
            try:
                if float(grade.maxValue) != gradeItem.maxPoints:
                    updateUrl = EDIT_GRADE_ITEM_URL.format(host=user.uc.host,gradeItemId=gradeItem.Id,courseId=course.Id)
                    message = 'Grade for {} is out of {}. The Max Points for {} is {}'.format(grade.studentName,grade.maxValue,gradeItem.name,gradeItem.maxPoints)
                    return render_template("updateGradeItem.html",gradeUrl=updateUrl,message=message)
                
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
            
    gradesUrl = VIEW_GRADES_URL.format(host=user.uc.host,gradeItemId=gradeItem.Id,courseId=course.Id)
    logoutUrl = LOGOUT_URL.format(host=user.uc.host)                     
    return render_template("gradesUploaded.html",errors=errors,successful_grades=successful_grades,grades=grades,course=course,gradeItem=gradeItem,gradesUrl=gradesUrl,logoutUrl=logoutUrl)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8080))
	app.run(host='0.0.0.0', port=port, debug=app_config["debug"])

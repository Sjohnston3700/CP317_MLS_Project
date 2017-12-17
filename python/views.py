'''
Functions used to render pages
'''
from app import app
from flask import render_template, redirect, request, session, abort
from conf_basic import app_config
from conf_basic import USER_ROLES
import traceback

from wrapper.obj.User import User
from wrapper.obj.Host import Host

LOGOUT_URL          = 'https://{host}/d2l/logout'

OUR_HOST = Host(app_config['lms_host'], versions=app_config['lms_ver'])
PAGES_NEEDING_LOGIN = ['token', 'courses', 'upload', 'report', 'logout']
DOCUMENTATION_PAGES = ['spmp','requirements','analysis','design','requirements_wrapper','analysis_wrapper','design_wrapper']
PAGES = PAGES_NEEDING_LOGIN + DOCUMENTATION_PAGES + ['help','login','documentation']


@app.route("/")
def start():
    '''
    Function runs at "/" URL, redirects to index.py.
    Postconditions:
        Redirect user to "/index.py".
    '''
    return redirect('/index.py')

@app.route("/index.py")
def index():
    '''
    Function to handle all page requests  via Get parameters
    '''
    #Get which page was requested
    page = request.args.get('page',None)
    
    if page in PAGES_NEEDING_LOGIN:
        #If it's the token page then pass off to authentication function
        if page == 'token':
            return auth_token_handler()
        
        #Check for valid user
        #If not logged in send them to home page
        if 'user_id' not in session and page != 'token':
            logger.warning('Someone tried to access {} but isn\'t logged in.'.format( request.url ) )
            return home(None)
        
        #if session is out of sync (eg. the server rebooted) send them to home
        elif app.config.get( session['user_id'], None) is None:
            logger.warning('Session is out of sync on {}.'.format( request.url) )
            return home(None)
        
    user = app.config.get( session.get('user_id',None), None)
        
        
    if page is None:
        return home(user)         
    else:
        if page not in PAGES:
            abort(404)
        elif page == 'help':
            return help(user)
        elif page == 'login':
            return login()
        elif page == 'logout':
            return show_logout(user);    
        elif page == 'courses':
            return show_courses(user)
        elif page == 'upload':
            return show_upload(user)
        elif page == 'report':
            return show_report(user)
        elif page == 'documentation':
            return show_docs(user)
        elif page in DOCUMENTATION_PAGES:
            return show_documentation(user, page)
            
    abort(404)#Should never be actually called
    


@app.errorhandler(Exception)
def handle_error(e):
    '''
    Default error handler. If something goes wrong in a route this gets called.
    Preconditions:
        e (Exception) : Exception that is being handled.
    Postconditions:
        Renders "error.html".
    '''
    user = app.config.get( session.get('user_id',None), None )
    return render_template('error.html',user=user,error=traceback.format_exc())


def home(user):
    '''
    Home page, Directs user to login or view docs.
    postconditions:
        Renders template of home.html.
    '''
    return render_template('home.html', user=user)
    

def help(user):
    '''
    Redirects user to help page.
    Postconditions:
        returns redirect to ezMarker help page.
    '''
    return render_template("help.html", user=user)

def login():
    '''
    Function redirects user to Brightspace secure login page to authenticate user.
    Postconditions:
        Redirect to Brightspace login page.
    '''
    trusted_url = '{0}://{1}:{2}{3}'.format(app_config['scheme'], app_config['host'], app_config['port'], app_config["route"])
    aurl = app.config["app_context"].create_url_for_authentication(app_config["lms_host"], trusted_url)
    return redirect(aurl)

def auth_token_handler():
    '''
    Authenticaion token handler - Creates User and user context.
    Postcontitions:
        On success:
            Redirect to "/index.py?page=courses".
        On failure:
            Renders "error.html".  
    '''
    uc = app.config["app_context"].create_user_context( result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])
    # store the user context's
    user    = User(uc, OUR_HOST, USER_ROLES)
    user_id = user.get_id()
    
    session['user_id']  = user_id
    app.config[user_id] = user
    return redirect('/index.py?page=courses')
    

def show_courses(user):
    '''
    Runs when application pointed to "/courses" URL.
    Postconditions:
        On success:
            If user_id in session : Renders "available_grades.html".
            Else : Redirects to "/login".
        On failure:
            Renders "error.html".
    '''
    return render_template('courses.html', user=app.config[ session['user_id'] ] )
    
    
def show_docs(user):
    '''
    Runs when application is pointed to "/documentation".
    Postconditions:
        Renders "documentation.html".
    '''
    return render_template('documentation.html',user=user)


def show_documentation(user, page):
    '''
    Function to display one of the documentation pages.
    '''
    assert page in DOCUMENTATION_PAGES, '{} is not a valid documentation page'.format(page)
    return render_template('index.html',user=user,doc=page)
    
def show_upload(user):
    """
    Displays the upload page.
    Preconditions:
        course_id (int) : Brightspace ID of current course. Passed through URL.
        gradeItemId (int) : Brightspace ID of current GradeItem. Passed through URL.
    Postconditions:
        if error with User:
            returns redirect to "/login".
        On success:
            Renders upload page.
        On failure:
            Renders error page.
    """
      
    course_id    = request.args.get('courseId',    default = None, type = int)
    grade_item_id = request.args.get('gradeItemId', default = None, type = int)

    course = user.get_course(course_id)
    grade_item = course.get_grade_item(grade_item_id)

    return render_template('upload.html',user=user,course=course,grade_item=grade_item)
    
def show_report(user):
    '''
    Displays report page.
    Postconditions:
        if error with user:
            Returns redirect to "/login"
        else:
            renders "report.html"
    '''
    
    course_id    = request.args.get('courseId',    default = None, type = int)
    grade_item_id = request.args.get('gradeItemId', default = None, type = int)
    
    course     = user.get_course(course_id)
    grade_item = course.get_grade_item( grade_item_id )
    
    key = '{}_report'.format( user.get_id() )
    report = app.config[key]
    num_grades = len(report['successful_grades']) + len(report['failed_grades'])
            
    return render_template('report.html', user=user,num_grades=num_grades, successful_grades=report['successful_grades'], failed_grades=report['failed_grades'],course=course,grade_item=grade_item)
    
def show_logout(user):
    '''
    Runs when application pointed to "/logout/" URL.
    Preconditions:
        course_id (int) : Brightspace ID of current course. Passed through URL.
        gradeItemId (int) : Brightspace ID of current GradeItem. Passed through URL.
    Postconditions:
        If user_id in session : redirects user to Brightspace logout page.
        Else : Redirects to "/login/".
    '''
    app.config.pop( session['user_id'] )
    session.clear()
    return redirect(LOGOUT_URL.format(host=app_config['lms_host']))

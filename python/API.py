import requests

SUCCESS = 200
API_ROUTE = '/d2l/api/versions/'
GET_GRADES_ROUTE     = '/d2l/api/le/(version)/(orgUnitId)/grades/'
SET_GRADE_ROUTE      = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)'
GET_COURSE_MEMBERS   = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/'
GET_USER_ENROLLMENTS = '/d2l/api/lp/(version)/enrollments/myenrollments/'
GET_USER_ENROLLMENT  = '/d2l/api/le/(version)/(orgUnitId)/grades/'
GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami'


def get_grade_items(course):
    '''
    Returns grades associated with the a given user context and course id number

    Preconditions:
        course (Course object) : the course to get the grade items for.
    '''
    # get latest installed version of the API
    product_code = 'lp'
    version =  [item['LatestVersion'] for item in get_api_versions(course.get_user().get_host()) if item['ProductCode'] == product_code][0]
    # Make request to get grades
    r = get_route(course.get_user(), GET_GRADES_ROUTE, {'version': version, 'orgUnitId': course.get_id() })
    # Check if request went through
    check_request(r)
    return r.json()

def put_grade_item(self, grade_item, params):
    '''
    Uses a PUT request to set multiple grade entries in Brightspace using JSON
    
    Preconditions :
        grade_item (GradeItem object) : The grade_item to change grade data for
        params (json) : JSON grade data to send
    Postconditions:
        Brightspace grade data will be changed for student with id user_id
    '''
    # get latest installed version of the API
    product_code = 'lp'
    version =  [item['LatestVersion'] for item in get_api_versions(grade_item.get_user().get_host()) if item['ProductCode'] == product_code][0]
    route_params = {'version': version, 'orgUnitId': grade_item.get_course().get_id(), 'gradeObjectId': grade_item.get_id()}
    r = put_route(grade_item.get_user(), SET_GRADES_ROUTE, route_params, params)
    check_request(r)
    return

def put_grade(self, us, user_id, course_id, grade_item_id, grade_data):
    '''
    Uses a PUT request to set a single grade entry for user 
	with ID = user_id in Brightspace using JSON
    
    Preconditions :
        uc : Usercontext to make the call with
        user_id (int or str) : Valence User Id of student
        course_id (int or str) : Valence Course Id number
        grade_item_id (int or str ) : Valence Grade Item Id
        grade_data (dict ) : JSON grade data to send
    Postconditions:
        Brightspace grade data will be changed for student with id user_id
    '''
    # get latest installed version of the API
    product_code = 'lp'
    version =  [item['LatestVersion'] for item in get_api_versions(uc) if item['ProductCode'] == product_code][0]
    route_params = {'version': version, 'orgUnitId': course_id, 'gradeObjectId': grade_item_id, 'userId': user_id}
	# Attempt to set the user's grade
    r = put_route(uc, SET_GRADE_ROUTE, route_params, grade_data)
    check_request(r)
    return

def update_route(route,params):
    '''
    Function to update api route by replace (...) with the appropriate value
    
    Preconditions: 
        route: the route from the valence docs (eg. '/d2l/api/le/(version)/(orgUnitId)/grades/')
        params: dictionary of replacement values (eg {'version':1.22,'orgUnitId':23456})

    Postconditions:
        Returns new route - Does not check for missed values
    '''
    for key in params:
        route = route.replace("({})".format( key ), str(params[key]) )
    return route

def get_route(user, route, params):
    ''' 
    Function to test api routes
        
    Preconditions :
        user: the user that is sending the request
        route: api route copied from valence doc
        params: dictionary of parameters - keys = what to replace

    Postconditions
        Returns :
            request result 
    '''    
    route = update_route(route,params)    
    url = user.get_context().create_authenticated_url(route,method='GET')
    return requests.get(url)

def put_route(user, route, params, data):
    ''' 
    Function to test api routes
    
    Preconditions :
        user: the user that is sending the request
        route: api route copied from valence docs
        params: dictionary of parameters - keys = what to replace
        data: python dictionary of json data to send

    Postconditions:
        Returns :
            request result 
    '''    
    route = update_route(route,params)
    url = user.get_context().create_authenticated_url(route,method='PUT')
    return requests.put(url,json=data)

def check_request(request):
    '''
    Function to test if a request was valid.

    Preconditions:
        request : the request object to test
    '''
    if request.status_code != SUCCESS:
        exception_message = 'Request returned status code : {}, text : {}'.format(request.status_code,request.text)
        raise  RuntimeError( exception_message )
    return    

def get_api_versions(host):
    '''
    Function to return the API versions available with this system

    Preconditions:
        host : The lms server we are connecting to
        scheme : http or https (dafault http)

    Postconditions:
        return :
             r.json() - json file contain all the supported versions
        Throws a RuntimeError if status code is not 200 
    '''
    r = requests.get('{}://{}/{}'.format(host.get_protocol(),host.get_lms_host(),API_ROUTE))
    check_request(r)
    return r.json()

def get_course_members(course):
    '''
    Function will return courses members for given course

    Preconditions:
        host : the lms server we are connecting to
        uc : Usercontext to make the call with
        courseId (str or int) : the course Id to get the course members from
        name (str) : The course name used for error messages (optional) 

    Postconditions:
        return :
            r.json()['items'] - Course Member for given course 
    '''
    host = course.get_user().get_host()
    r = get_route(course.get_user(),GET_COURSE_MEMBERS,{'version': host.get_api_version('lp'),'orgUnitId':course.get_id()})
    check_request(r)
    return r.json()['Items']

def get_user_enrollments(user):
    '''
    Function will return the list of all enrollments for the current user

    Preconditions:
        user: The current user to which we are getting enrollments for

    Postconditions:
        return:
            r.json - json file containing all enrollments for the current user
    '''
    r = get_route(user, GET_USER_ENROLLMENTS, {'version': user.get_host().get_api_version('lp')})
    check_request(r)
    return [item for item in r.json()["Items"] if item['OrgUnit']['Type']['Code'] == 'Course Offering']

def get_user_enrollment(user, course_id):
    '''
    Function will retrieve all the current grade objects for a particular course id

    Preconditions:
        user: The current user 
        course_id: Integer ID of a given course

    Postconditions:
        return:
            r.json() - a json array of grade objects blocks.
    '''
    r = get_route(user,GET_USER_ENROLLMENT,{'version': user.get_host().get_api_version('le'),'orgUnitId': course_id})
    check_request(r)
    return r.json()

def get_who_am_i(user):
    '''
    Function retrieves the current user context's user information

    Preconditions:
        user: the current user
        
    Postconditions:
        return:
            r.json() - json file containing user data of the current user
    '''
    r = get_route(user, GET_WHO_AM_I,{'version': user.get_host().get_api_version('lp')})
    check_request(r)
    return r.json()

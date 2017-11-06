import requests

SUCCESS = 200
API_ROUTE = '/d2l/api/versions/'
GET_GRADES_ROUTE     = '/d2l/api/le/(version)/(orgUnitId)/grades/'
SET_GRADE_ROUTE      = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)'
GET_COURSE_MEMBERS   = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/'
GET_USER_ENROLLMENTS = '/d2l/api/lp/(version)/enrollments/myenrollments/'
GET_USER_ENROLLMENT  = '/d2l/api/le/(version)/(orgUnitId)/grades/'
GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami'


def get(route, user = None, route_params = None):
    '''
    Uses a GET request to get JSON

    Preconditions:
        user - A User object corresponding to the current user
        route - The route to make a GET request to
        route_params - A dictionary of parameters corresponding to route
    Postconditions
        On success:
            Returns:
            Python dict of grade objects
        On failure:
            raises RuntimeError
    '''
    # For making a call which does not require User context
    if user is None:
        r = requests.get(update_route(route, route_params))
    else:
        # Make request to GET grades
        r = get_route(user, route, route_params)
    # Check if request was valid
    check_request(r)
    return r.json()

def put(route, user, route_params, params):
    '''
    Uses a PUT request to set JSON
    
    Preconditions :
        grade_item (GradeItem object) : The grade_item to change grade data for
        params (json) : JSON grade data to send
    Postconditions:
        Brightspace data will be updated with params as JSON
    '''
    # Make request to PUT grades
    r = put_route(user, route, route_params, params)
    # Check if request was valid
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

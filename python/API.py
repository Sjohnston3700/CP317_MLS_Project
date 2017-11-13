import requests

SUCCESS = 200

API_ROUTE            = '/d2l/api/versions/'
GET_GRADES_ROUTE     = '/d2l/api/le/(version)/(orgUnitId)/grades/'
SET_GRADEITEM_ROUTE  = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)'
SET_GRADE_ROUTE      = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)'
GET_COURSE_MEMBERS   = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/'
GET_USER_ENROLLMENTS = '/d2l/api/lp/(version)/enrollments/users/(userId)/orgUnits/'
GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami'


def get(route, user = None, route_params = {},additional_params={}):
    '''
    Uses a GET request to get JSON

    Preconditions:
        user - A User object corresponding to the current user
        route - The route to make a GET request to
        route_params - A dictionary of parameters corresponding to route
        additional_params - A dictionary of extra parameters. Added to the end of the url as ?key=value
    Postconditions
        On success:
            Returns:
            Python dict of request result
        On failure:
            raises RuntimeError
    '''
    route = update_route(route, route_params)
    if user is not None:
        route = user.get_context().create_authenticated_url(route,method='GET')
    r = requests.get(route, additional_params=payload)
    
    check_request(r)
    
    results = r.json()
    if 'PagingInfo' in results.keys() and results['PagingInfo']['HasMoreItems'] == True:
        bookmark = results['PagingInfo']['Bookmark']
        next_results = get(route, user,route_params,{'Bookmark':bookmark})        
        results['Items'] += next_results['Items']
        
    return results

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
    route = update_route(route,route_params)
    r = requests.put(user.get_context().create_authenticated_url(route,method='PUT'),json=params)
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
    if params is not None:#Dont care about params={} for loop takes care of it
        for key in params:
            route = route.replace("({})".format( key ), str(params[key]) )
 
    if '(' in route or ')' in route:#check for missed stuff to replace
        exception_message = 'Route : {} needs more parameters'.format(route)
        raise  RuntimeError( exception_message )
    return route

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

def get_grade_items(course):
    '''
    Gets grade item JSON as python dict from a Course object
    
    Preconditions:
        course : the Course to retrieve grades from
    Postconditions:
        returns
        a dict of grade items corresponding to the given course
    '''
    user = course.get_user()
    route_params = {'version' : user.get_host().get_api_version('le'), 'orgUnitId': course.get_id()}
    r = get(GET_GRADES_ROUTE, user, route_params)
    return r
    
def put_grade(grade):
    '''
    Posts a Grade object to Brightspace using a PUT request
    
    Preconditions:
        grade : the grade to post
    Postconditions:
        grade JSON is PUT to Brightspace
    '''
    user = grade.get_user()
    route_params = {'version' : user.get_host().get_api_version('le'), \
        'orgUnitId': grade.get_grade_item().get_course().get_id(), \
        'gradeObjectId': grade.get_grade_item().get_id(), \
        'userId' : grade.get_student().get_id() }
    params = {"Comments": grade.get_comment(), "PrivateComments": ''} # For generic Grade
    
    # TODO: Support other Grade types?
    params['GradeObjectType'] = 1 # NumericGrade Type
    params['PointsNumerator'] = grade.get_value() # For NumericGrade
    
    # Make PUT request
    r = put(SET_GRADE_ROUTE, user, route_params, params)
    return

def put_grade_item(grade_item):
    '''
    Posts a GradeItem object to Brightspace using a PUT request
    
    Preconditions:
        grade_item : the grade_item to post
    Postconditions:
        grade_item JSON is PUT to Brightspace
    '''
    user = grade_item.get_user()
    route_params = {'version' : user.get_host().get_api_version('le'), \
            'orgUnitId': grade.get_grade_item().get_course().get_id(), \
            'gradeObjectId': grade.get_grade_item().get_id() }
    params = { "MaxPoints": grade_item.get_max(), "CanExceedMaxPoints": grade_item.can_exceed(), "GradeType": "Numeric" }
    r = put(SET_GRADEITEM_ROUTE, user, route_params, params)
    return
    
def get_api_versions(host):
    '''
    Gets product version numbers JSON as python dict 
    
    Preconditions:
        host : the Host object used
    Postconditions:
        returns
        a dict of product version numbers for the API
    '''
    r = get('{}://{}/{}'.format(host.get_protocol(),host.get_lms_host(), API_ROUTE))
    return r

def get_user_enrollments(user):
    '''
    Retrieves the collection of users enrolled in the identified org unit.
    
    Preconditions:
        course : the Course to retrieve grades from
    Postconditions:
        returns
        a dict of grade items corresponding to the given course
    '''
    route_params = {'version':unser.get_host().get_api_version('lp'), 'userId':user.get_id()}
    r = get(GET_USER_ENROLLMENTS, user, route_params)
    user_enrollments = r['Items']
    return user_enrollments

def get_who_am_i(user):
    '''
    Retrieve the current user context’s user information as python dict JSON.
    
    Preconditions:
        user : the Course to retrieve grades from
    Postconditions:
        returns
         WhoAmIUser JSON block for the current user context (as python dict)
    '''
    route_params = {'version' : user.get_host().get_api_version('lP')}
    r = get(GET_WHO_AM_I, user, route_params)
    return
    
    

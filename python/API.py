import requests

SUCCESS = 200

API_ROUTE            = '/d2l/api/versions/'
GET_GRADES_ROUTE     = '/d2l/api/le/(version)/(orgUnitId)/grades/'
SET_GRADEITEM_ROUTE  = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)'
SET_GRADE_ROUTE      = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)'
GET_COURSE_MEMBERS   = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/'
GET_USER_ENROLLMENTS = '/d2l/api/lp/(version)/enrollments/users/(userId)/orgUnits/'
GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami'

def check_request(request):
    '''
    Function to test if a request was valid.

    Preconditions:
        request (str) : the request object to test.
        
    Postconditions:
        on success:
            Request returns a valid SUCCESS status code, is a valid request.
        on failure:
            raises RuntimeError.
    '''
    if request.status_code != SUCCESS:
        exception_message = 'Request returned status code : {}, text : {}'.format(request.status_code,request.text)
        raise  RuntimeError( exception_message )
    return 

def get(route, user = None, route_params = {},additional_params={}):
    '''
    Uses a GET request to get JSON.

    Preconditions:
        user (User object) : A User object corresponding to the current user.
        route (str) : The route to make a GET request to.
        route_params (dict) : A dictionary of parameters corresponding to route.
        additional_params (dict): A dictionary of extra parameters. Added to the end of the url as ?key=value.
        
    Postconditions
        On success:
            Returns:
            results (dict) : Python dict of JSON data from request result.
        On failure:
            raises RuntimeError
    '''
    route = update_route(route, route_params)
    if user is not None:
        route = user.get_context().create_authenticated_url(route,method='GET')
    r = requests.get(route, params=additional_params)
    
    check_request(r)
    
    results = r.json()
    if 'PagingInfo' in results and results['PagingInfo']['HasMoreItems'] == True:
        bookmark = results['PagingInfo']['Bookmark']
        next_results = get(route, user,route_params,additional_params={'Bookmark':bookmark})        
        results['Items'] += next_results['Items']
        
    return results

def put(route, user, route_params, params):
    '''
    Uses a PUT request to set JSON.
    
    Preconditions :
        user (User object) : A User object corresponding to the current user.
        route (str) : The route to make a GET request to.
        route_params (dict) : A dictionary of parameters corresponding to route.
        params (dict) : A dictionary of JSON grade data to send.
        
    Postconditions:
        Brightspace data will be updated with params as JSON.
    '''
    # Make request to PUT grades
    route = update_route(route,route_params)
    r = requests.put(user.get_context().create_authenticated_url(route,method='PUT'),json=params)
    # Check if request was valid
    check_request(r)
    return

def update_route(route,params):
    '''
    Function to update api route by replace (...) with the appropriate value.
    
    Preconditions: 
        route (str) : The route to make a GET/PUT request to.
        params (dict) : A dictionary of parameters corresponding to route.

    Postconditions:
        On success:
            Returns:
            route (str) : Updated route with params inserted. 
        On failure:
            raises RuntimeError.
    '''
    if params is not None:#Dont care about params={} for loop takes care of it
        for key in params:
            route = route.replace("({})".format( key ), str(params[key]) )
 
    if '(' in route or ')' in route:#check for missed stuff to replace
        exception_message = 'Route : {} needs more parameters'.format(route)
        raise  RuntimeError( exception_message )
    return route   

def get_api_versions(host):
    '''
    Gets product version numbers JSON as python dict. 
    
    Preconditions:
        host (Host object) : A Host object corresponding to the current host.

    Postconditions:
        returns:
        results (dict) : A dict of product version numbers for the API.
    '''
    results = get('{}://{}/{}'.format(host.get_protocol(),host.get_lms_host(), API_ROUTE))
    return results
    
 
def get_grade_items(course):
    '''
    Gets grade item JSON as python dict from a Course object.
    
    Preconditions:
        course (Course object) : The Course object to retrieve GradeItems for.
        
    Postconditions:
        returns:
        results (dict) : Python dict of JSON data containing GradeItem object data for the given course.
    '''
    user = course.get_user()
    route_params = {'version' : user.get_host().get_api_version('le'), 'orgUnitId': course.get_id()}
    results = get(GET_GRADES_ROUTE, user, route_params)
    return results
    
def get_user_enrollments(user):
    '''
    Retrieves the collection of users enrolled in the identified org unit.
    
    Preconditions:
        course (Course object) : A Course object to retrieve grades from.
        
    Postconditions:
        returns:
        user_enrollments (dict) : A dict of user_enrollment data corresponding to the given User object.
    '''
    route_params = {'version':unser.get_host().get_api_version('lp'), 'userId':user.get_id()}
    r = get(GET_USER_ENROLLMENTS, user, route_params)
    user_enrollments = r['Items']
    return user_enrollments

def get_who_am_i(user):
    '''
    Retrieve the current user context’s user information as python dict JSON.
    
    Preconditions:
        user (User object) : A User object corresponding to the current user.
        
    Postconditions:
        returns:
        Results (dict) : A dict containing WhoAmIUser JSON block for the current user context. 
    '''

    route_params = {'version' : user.get_host().get_api_version('lp')}
    results = get(GET_WHO_AM_I, user, route_params)
    return results
    
def put_grade(grade):
    '''
    Posts a Grade object to Brightspace using a PUT request.
    
    Preconditions:
        grade (Grade object) : the Grade object to post to Brightspace.
        
    Postconditions:
        Grade object data as JSON is PUT to Brightspace.
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
    Posts a GradeItem object to Brightspace using a PUT request.
    
    Preconditions:
        grade_item (GradeItem object) : the GradeItem object to post to Brightspace.
        
    Postconditions:
        grade_item data as JSON is PUT to Brightspace.
    '''
    user = grade_item.get_user()
    route_params = {'version' : user.get_host().get_api_version('le'), \
            'orgUnitId': grade.get_grade_item().get_course().get_id(), \
            'gradeObjectId': grade.get_grade_item().get_id() }
    params = { "MaxPoints": grade_item.get_max(), "CanExceedMaxPoints": grade_item.can_exceed(), "GradeType": "Numeric" }
    r = put(SET_GRADEITEM_ROUTE, user, route_params, params)
    return

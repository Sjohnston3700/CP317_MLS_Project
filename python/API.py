import requests

SUCCESS = 200
API_ROUTE = '/d2l/api/versions/'
GET_GRADES_ROUTE     = '/d2l/api/le/(version)/(orgUnitId)/grades/'
SET_GRADE_ROUTE      = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)'
GET_COURSE_MEMBERS   = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/'
GET_USER_ENROLLMENTS = '/d2l/api/lp/(version)/enrollments/myenrollments/'
GET_USER_ENROLLMENT  = '/d2l/api/le/(version)/(orgUnitId)/grades/'
GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami'


def get(route, user = None, route_params = {}):
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
        route = update_route(route, route_params)
        r = requests.get(user.get_context().create_authenticated_url(route,method='GET'))
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

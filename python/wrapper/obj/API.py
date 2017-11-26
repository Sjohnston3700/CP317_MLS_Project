import requests, traceback, sys,logging

#Can't do from Course import Course etc. It creates cirular imports and breaks the universe
import Course
import GradeItem
import OrgMember

SUCCESS = 200

API_ROUTE            = '/d2l/api/versions/'
SET_GRADEITEM_ROUTE  = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)'
GET_GRADE_ITEMS      = '/d2l/api/le/(version)/(orgUnitId)/grades/'
SET_GRADE_ROUTE      = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)'
GET_COURSE_MEMBERS   = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/'
GET_USER_ENROLLMENTS = '/d2l/api/lp/(version)/enrollments/users/(userId)/orgUnits/'
GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami'

logger = logging.getLogger(__name__)

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
        exception_message = 'Request {} returned status code : {}, text : {}'.format(request.url,request.status_code,request.text)
        raise  RuntimeError( exception_message )
    return 

def get(route, user, route_params = {},additional_params={}):
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
    route = user.get_context().create_authenticated_url(route,method='GET')
    r = requests.get(route, params=additional_params)
    
    check_request(r)
    
    results = r.json()
    if 'PagingInfo' in results and results['PagingInfo']['HasMoreItems'] == True:
        bookmark = results['PagingInfo']['Bookmark']
        next_results = get(route, user,route_params,additional_params={'Bookmark':bookmark})        
        results['Items'] += next_results['Items']
        
    return results

def get_class_list(course):#is this the right name for this function?
    '''
    Function to take a course object and return a list of enolled org members
    
    Preconditions:
        course : course object
    Postconditions:
        returns list of enrolled orgMember objects empty if None found our all died horrible deaths on creation
    '''
    try:
        json = get(GET_COURSE_MEMBERS,course.get_user(),{'orgUnitId':course.get_id(),'version': course.get_user().get_host().get_api_version('lp')})    
        members = []
        for member in json['Items']:
            try:
                members.append( OrgMember.OrgMember(member) )
            except Exception as e:
                logging.error("Unable to create Orgmember from {}. {}".format(member,e) )
                continue
        return members
    except Exception as e:
        logging.error("Something went wrong in get_class_list. {}".format(e) )
        raise
        return None
    
def get_courses(user,roles=[]):
    '''
    Function to get all courses a logged in user is enrolled in (has accesss to)
    
    Preconditions:
        user (User object) - logged in user
        roles (list (eg : ['Instructor','TA','Student']) ) - roles to filter by, not yet implimented
    Postconditions:
        courses (list of Course objects) - list of enrolled courses, empty if none found or all failed for some reason which is logged
    '''
    try:
        json = get(GET_USER_ENROLLMENTS,user,{'version':user.get_host().get_api_version('le'),'userId': user.get_id()})
        courses = []
        for item in json['Items']:
            try:
                courses.append( Course.Course(user,item) )
            except Exception as e:
                continue
        logger.info("Extracted {} of {} courses for {}".format( len(courses),len(json["Items"]),user.get_name() ) )
        return courses
    except Exception as e:
        logging.error("Something went wrong in get_courses. {}".format(e) )
        raise
        return None


def get_grade_items(course):
    """
    Function will return list of grade items
    return :
            lists - grade item (Array of grade item object) - currenlty only supports Numeric
    """
    gradeitems = get(GET_GRADE_ITEMS,course.get_user(),{'orgUnitId':course.get_id(),'version':course.get_user().get_host().get_api_version('le')})
    items = []
    for item in gradeitems:
        if item['GradeType'] == 'Numeric':
            items.append( GradeItem.NumericGradeItem(course, item) )
    return items


def get_who_am_i(user):
    '''
    Retrieve the current user context's user information as python dict JSON.
    
    Preconditions:
        user (User object) : A User object corresponding to the current user.
        
    Postconditions:
        returns:
        Results (dict) : A dict containing WhoAmIUser JSON block for the current user context. 
    '''

    route_params = {'version' : user.get_host().get_api_version('lp')}
    results = get(GET_WHO_AM_I, user, route_params)
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
    
    data = grade.get_json()
    # Make PUT request
    put(SET_GRADE_ROUTE, user, route_params, data)
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
            'orgUnitId': grade_item.get_course().get_id(), \
            'gradeObjectId': grade_item.get_id() }

    data = grade_item.get_json()
    put(SET_GRADEITEM_ROUTE, user, route_params, data)
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
    

import requests, traceback, sys, logging

#Can't do from Course import Course etc. It creates circular imports and breaks the universe
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
GET_MY_ENROLLMENTS   = '/d2l/api/lp/(version)/enrollments/myenrollments/'
GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami'


logger = logging.getLogger(__name__)

def check_request(request):
    '''
    Function to test if a request was valid.

    Preconditions:
        request (str) : The request object to test.
        
    Postconditions:
        On success:
            Request returns a valid SUCCESS status code, is a valid request.
        On failure:
            Raises RuntimeError.
    '''
    if request.status_code != SUCCESS:
        exception_message = 'Request {} returned status code : {}, text : {}'.format(request.url, request.status_code, request.text)
        raise  RuntimeError( exception_message )
    return 

def get(route, user, route_params = {}, additional_params = {}):
    '''
    Uses a GET request to get JSON.

    Preconditions:
        user (User) : A User object corresponding to the current user.
        route (str) : The route to make a GET request to.
        route_params (dict) : A dictionary of parameters corresponding to route.
        additional_params (dict): A dictionary of extra parameters. Added to the end of the url as ?key=value.
        
    Postconditions:
        On success:
            Returns:
            results (dict) : Python dict of JSON data from request result.
        On failure:
            Raises RuntimeError.
    '''
    updated_route = update_route(route, route_params)
    auth_route = user.get_context().create_authenticated_url(updated_route, method='GET')
    r = requests.get(auth_route, params=additional_params)
    
    check_request(r)
    
    results = r.json()
    if 'PagingInfo' in results and results['PagingInfo']['HasMoreItems'] == True:
        bookmark = results['PagingInfo']['Bookmark']
        next_results = get(route, user,route_params,additional_params={'Bookmark':bookmark})        
        results['Items'] += next_results['Items']
        
    return results

#is this the right name for this function?
def get_class_list(course):
    '''
    Function to take a course object and return a list of enrolled OrgMembers.
    
    Preconditions:
        course (Course) : A Course object.
    Postconditions:
        On success:
            Returns: 
            members (list of OrgMembers) : List of enrolled OrgMember objects.
        On failure:
            Returns:
            None if empty class or all died horrible deaths on creation.
    '''
    try:
        json = get(GET_COURSE_MEMBERS, course.get_user(), {'orgUnitId':course.get_id(), 'version': course.get_user().get_host().get_api_version('lp')})    
        members = []
        for member in json['Items']:
            try:
                members.append( OrgMember.OrgMember(member) )
            except Exception as e:
                logging.error("Unable to create OrgMember from {}. {}".format(member, e) )
                continue
        return members
    except Exception as e:
        logging.error("Something went wrong in get_class_list. {}".format(e) )
        raise
        return None
    
def get_courses(user, roles=[]):
    '''
    Function to get all courses a logged in user is enrolled in (has access to).
    
    Preconditions:
        user (User) : Logged in user.
        roles (list (eg : ['Instructor', 'TA', 'Student']) ) : Roles to filter by, not yet implemented.
    Postconditions:
        On success:
            Returns:
            courses (list of Course objects) : List of courses user is enrolled in (has access to).
        On failure:
            Returns:
            None if user has no classes or all failed for some reason and is logged.
    '''
    try:
        json = get(GET_USER_ENROLLMENTS, user, { 'version':user.get_host().get_api_version('lp'), 'userId':user.get_id() })
        courses = []
        for item in json['Items']:
            try:
                if item['OrgUnit']['Type']['Name'] == 'Course Offering' and (roles== [] or  item['Role']['Name'] in roles):
                    courses.append( Course.Course(user, item) )
            except Exception as e:
                continue
        logger.info("Extracted {} of {} courses for {}".format( len(courses), len(json["Items"]), user.get_full_name() ) )
        return courses
    except Exception as e:
        logging.error("Something went wrong in get_courses. {}".format(e) )
        raise
        return None


def get_grade_items(course):
    '''
    Function to return list of grade items.
    
    Preconditions:
        course (Course) : A Course object.
    
    Postconditions:
            Returns:
            list (list of grade item objects) : currently only supports Numeric.
    '''
    gradeitems = get(GET_GRADE_ITEMS, course.get_user(), {'orgUnitId':course.get_id(), 'version':course.get_user().get_host().get_api_version('le')})
    items = []
    for item in gradeitems:
        if item['GradeType'] == 'Numeric':
            items.append( GradeItem.NumericGradeItem(course, item) )
    return items


def get_who_am_i(user):
    '''
    Retrieves the current user context's user information as python dict JSON.
    
    Preconditions:
        user (User) : A User object corresponding to the current user.
        
    Postconditions:
        Returns:
        results (dict) : A dictionary containing WhoAmIUser JSON block for the current user context. 
    '''

    route_params = {'version' : user.get_host().get_api_version('lp')}
    results = get(GET_WHO_AM_I, user, route_params)
    return results

def put(route, user, route_params, params):
    '''
    Uses a PUT request to set JSON.
    
    Preconditions :
        user (User) : A User object corresponding to the current user.
        route (str) : The route to make a GET request to.
        route_params (dict) : A dictionary of parameters corresponding to route.
        params (dict) : A dictionary of JSON grade data to send.
        
    Postconditions:
        Brightspace data will be updated with params as JSON.
    '''
    # Make request to PUT grades
    route = update_route(route, route_params)
    r = requests.put(user.get_context().create_authenticated_url(route, method='PUT'), json=params)
    # Check if request was valid
    try:
        check_request(r)
    except Exception as e:
        raise
    return

def put_grade(grade):
    '''
    Posts a Grade object to Brightspace using a PUT request.
    
    Preconditions:
        grade (Grade) : The Grade object to post to Brightspace.
        
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

def put_grades(grades):
    '''
    Function to post a list of grade objects to Brightspace
    
    Preconditions:
        grades (list of grade objects) : The Grade objects to post
    
    Postconditions:
        Returns:
        successful_grades (list of Grade objects that didn't return errors)
        failed_grades (list of dictionary objects) msg key holds error message, grade key holds grade object that failed
    '''
    successful_grades = []
    failed_grades     = []
    for grade in grades:
        try:
            put_grade(grade)
            successful_grades.append( grade )
        except Exception as e:
            error = {'msg':str(e),'grade':grade}
            failed_grades.append( error )
    return successful_grades, failed_grades
    
def put_grade_item(grade_item):
    '''
    Posts a GradeItem object to Brightspace using a PUT request.
    
    Preconditions:
        grade_item (GradeItem) : The GradeItem object to post to Brightspace.
        
    Postconditions:
        grade_item data as JSON is PUT to Brightspace.
    '''
    user = grade_item.get_user()
    route_params = {'version' : user.get_host().get_api_version('le'), \
            'orgUnitId': grade_item.get_course().get_id(), \
            'gradeObjectId': grade_item.get_id() }
    
    
    data = grade_item.get_json()
    to_remove = ['Weight', 'GradeSchemeUrl', 'Id', 'ActivityId']
    for item in to_remove:
        data.pop(item, None)
    
    data['Description']={'Content' : data['Description']['Html'], 'Type':'Html'}
    
    put(SET_GRADEITEM_ROUTE, user, route_params, data)
    return
    
def update_route(route, params):
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
    
    # Dont care about params={} for loop takes care of it
    if params is not None:
        for key in params:
            route = route.replace("({})".format( key ), str(params[key]) )

    if '(' in route or ')' in route:#check for missed stuff to replace
        exception_message = 'Route : {} needs more parameters'.format(route)
        raise  RuntimeError( exception_message )
    return route   
    

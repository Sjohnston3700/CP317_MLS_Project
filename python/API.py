import requests

SUCCESS = 200
API_ROUTE = '/d2l/api/versions/'
GET_CLASSES_ROUTE    = '/d2l/api/lp/(version)/enrollments/myenrollments/'
GET_GRADES_ROUTE     = '/d2l/api/le/(version)/(orgUnitId)/grades/'
SET_GRADE_ROUTE      = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)'
GET_COURSE_MEMBERS   = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/'
GET_USER_ENROLLMENTS = '/d2l/api/lp/(version)/enrollments/myenrollments/'
GET_USER_ENROLLMENT  = '/d2l/api/le/(version)/(orgUnitId)/grades/'
GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami'

class ValenceAPI(object):
    '''
    Class to make using the Valence API a little easier.
    '''
    
    def __init__(self,host,scheme='http',debug=True):
        '''
        Preconditions:
            host : The lms server we are connecting to
            scheme : http or https (default http)
            debug - do failed requests print the code and text on failing or just a message (default=True)
        '''
        self.host     = host
        self.scheme   = scheme
        self.debug    = debug
        self.versions = self.getApiVersions()

        
    def getApiVersions(self):
        '''
        Function to return the Api versions available with this system
        
        Preconditions:
            uc (user context) : The user context to call this with
        
        Postcondtions:
            returns : r.json()
            Throws a RuntimeError if status code is not 200
        '''
        r=requests.get( '{}://{}/{}'.format(self.scheme,self.host,API_ROUTE) )
        checkRequest(r,"Unable to download API versions",self.debug)
        return r.json()
            
    def getApiVersion(self,productCode):
        '''
        Function to extract API version for a specific call
        
        Preconditions :
            productCode : the product code to look for.
        Postconditions :
            Returns the latest version if found. Crashes horribly if not found
        '''
        return [item['LatestVersion'] for item in self.versions if item['ProductCode']==productCode][0]
    
            
    def getCourses(self,uc):
        '''
        Function to return courses associated with the current user context
        
        Preconditions:
            uc : Usercontext to make the call with
        '''
        r = getRoute( uc,GET_CLASSES_ROUTE, {'version': self.getApiVersion('lp') } )
        checkRequest(r,"Unable to download Classes",self.debug)
        return [item for item in r.json()["Items"] if item['OrgUnit']['Type']['Code']=='Course Offering' ]
        
    def getGradeItems(self,uc,courseId,name=""):
        '''
        Function to return grades associated with the current user context and given courseId
        Precondtions:
            uc : Usercontext to make the call with
            courseId (str or int) : the course Id to get the grade items for.
            name (str) : The course name used for error messages (optional)
        '''
        r=getRoute( uc,GET_GRADES_ROUTE, {'version': self.getApiVersion('lp'), 'orgUnitId':courseId } )
        checkRequest(r,"Unable to download Grade Items for {} (Id:{})".format(name,courseId),self.debug)
        return r.json()
        
    def setGrade(self,uc,userId,courseId,gradeItemId,grade_data):
        '''
        Function to set a user grade
        
        Preconditions :
            uc : Usercontext to make the call with
            userId (int or str) : Valence User Id
            courseId (int or str) : Valence Course Id number
            gradeItemId (int or str ) : Valence Grade Item Id
            grade_data (dict ) : Correctly formatted json to send
        '''
        route_params = {'version': self.getApiVersion('lp'), 'orgUnitId':courseId, 'gradeObjectId':gradeItemId,'userId':userId }
        r = putRoute(uc,SET_GRADE_ROUTE,route_params,grade_data)
        checkRequest(r,"Unable to set grade for user {}".format(userId),self.debug)
        return
        
       
         
def updateRoute(route,params):
    '''
    Function to update api route by replace (...) with the appropriate value
    
    Preconditions: 
    route - the route from the valence docs (eg. '/d2l/api/le/(version)/(orgUnitId)/grades/')
    params - dictionary of replacement values (eg {'version':1.22,'orgUnitId':23456})

    Postconditions:
    Returns new route - Does not check for missed values
    '''
    for key in params:
        route = route.replace("({})".format( key ), str(params[key]) )
    return route

            
def getRoute(uc, route, params):
    ''' 
    Function to test api routes
        
    Preconditions :
        uc - the user context
        route - api route copied from valence docs
        params - dictionary of parameters - keys = what to replace

    Postconditions
        Returns :
            request result 
    '''    
    route = updateRoute(route,params)
        
    url = uc.create_authenticated_url(route,method='GET')
    return requests.get(url)

def putRoute(uc, route, params,data):
    ''' 
    Function to test api routes
    
    Preconditions :
    uc - the user context
    route - api route copied from valence docs
    params - dictionary of parameters - keys = what to replace
    data - python dictionary of json data to send

    Returns :
    request result 
    '''    
    route = updateRoute(route,params)
    
    url = uc.create_authenticated_url(route,method='PUT')
    return requests.put(url,json=data)           
    
def checkRequest(r,err_message,debug=True):
    '''
    Function to test if a request was valid.
    Preconditions:
        r : the request object to test
        err_message : The error message to display
        debug  : Do we also display the status code and text?
    '''
    if r.status_code != SUCCESS:
        exception_message = err_message
        exception_message += 'Request returned status code : {}, text : {}'.format(r.status_code,r.text) if debug else ""
        raise  RuntimeError( exception_message )
    return

#********************************************************************************************************************************
# TODO: OLD CODE ENDS HERE 
#********************************************************************************************************************************


def get_grade_items(uc, course_id):
    '''
    Returns grades associated with the a given user context and course id number

    Preconditions:
        uc : Usercontext to make the call with
        course_id (str or int) : the course Id to get the grade items for.
    '''
    # get latest installed version of the API
    product_code = 'lp'
    version =  [item['LatestVersion'] for item in get_api_versions(uc) if item['ProductCode'] == product_code][0]
    # Make request to get grades
    r = get_route(uc, GET_GRADES_ROUTE, {'version': version, 'orgUnitId': course_id })
    # Check if request went through
    check_request(r, "Unable to download Grade Items for course (Id:{})".format(course_id))
    return r.json()

def put_grade_item(self, uc, course_id, grade_item_id):
    '''
    Uses a PUT request to set multiple grade entries in Brightspace using JSON
    
    Preconditions :
        uc : Usercontext to make the call with
        course_id (int or str) : Valence Course Id number
        grade_item_id (int or str ) : Valence Grade Item Id
        grade_data (dict ) : JSON grade data to send
    Postconditions:
        Brightspace grade data will be changed for student with id user_id
    '''
    # get latest installed version of the API
    product_code = 'lp'
    version =  [item['LatestVersion'] for item in get_api_versions(uc) if item['ProductCode'] == product_code][0]
    route_params = {'version': version, 'orgUnitId': course_id, 'gradeObjectId': grade_item_id}
    r = put_route(uc, SET_GRADES_ROUTE, route_params, grade_data)
    check_request(r, "Unable to set grade for course {}".format(course_id))
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
    check_request(r, "Unable to set grade for user {}".format(user_id))
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
        r : the request object to test
    '''
    if r.status_code != SUCCESS:
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
    r = requests.get('{}//{}/{}'.format(host.get_protocol(),host.get_lms_host(),API_ROUTE))
    checkRequest(r)
    return r.json()

def get_course_member(course):
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
    return r.json()['items']

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
    return r.json()

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

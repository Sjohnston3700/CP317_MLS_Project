import requests

SUCCESS = 200
API_ROUTE = '/d2l/api/versions/'
GET_CLASSES_ROUTE  = '/d2l/api/lp/(version)/enrollments/myenrollments/'
GET_GRADES_ROUTE   = '/d2l/api/le/(version)/(orgUnitId)/grades/'
SET_GRADE_ROUTE    = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)'
GET_COURSE_MEMBERS = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/'

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


def getApiVersions(host,scheme='http'):
    '''
    Function to return the API versions available with this system

    Postconditions:
        host : The lms server we are connecting to
        scheme : http or https (dafault http)

    Postconditions:
        return :
             r.json() json file contain all the supported versions
        Throws a RuntimeError if status code is not 200 
    '''
    r = requests.get('{}://{}/{}'.format(scheme,host,API_ROUTE))
    checkRequest(r,"Unable todownload API versions")
    return r.json()

def getCourseMember(uc,courseId,host,name = ""):
    '''
    Function will return courses members for given course

    Postconditions:
        host : the lms server we are connecting to
        uc : Usercontext to make the call with
        courseId (str or int) : the course Id to get the course members from
        name (str) : The course name used for error messages (optional) 

    Preconditions:
        return : Course Member for given course
    '''
    r = getRoute(uc,GET_COURSE_MEMBERS,{'version': host.get_api_version('lp'),'orgUnitId':courseId})
    checkRequest(r,"Unable to download Course Members for {} (Id:{})".format(name,courseId))
    return r.json()['items']
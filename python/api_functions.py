import requests

SUCCESS = 200
API_ROUTE = '/d2l/api/versions/'



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
    
    
def getApiVersions(uc):
    '''
    Function to return the Api versions available with this system
    
    Preconditions:
        uc (user context) : The user context to call this with
    
    Postcondtions:
        returns : r.json()
        Throws a RuntimeError if status code is not 200
    '''
    r=getRoute(uc,API_ROUTE,{})
    if r.status_code != SUCCESS:
        raise RuntimeError('Unable to download API versions. Request returned status code : {}, text : {}'.format(r.status_code,r.text) )
    else:
        return r.json() 
        
        
def getAvailableClasses(uc):
    '''
    Function to return the Api versions available with this system
    
    Preconditions:
        uc (user context) : The user context to call this with
    
    Postcondtions:
        returns : r.json()
        Throws a RuntimeError if status code is not 200
    '''
    
    


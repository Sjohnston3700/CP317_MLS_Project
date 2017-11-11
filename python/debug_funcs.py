import requests
import requests
import d2lvalence.auth as d2lauth
import json
from conf_basic import app_config as config

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
    for key in params:
        route = route.replace("({})".format( key ), str(params[key]) )
    
    url = uc.create_authenticated_url(route,method='GET')
    return requests.get(url)

def putRoute(uc, route, params,data):
    ''' 
    Function to test api routes
    
    Preconditions :
    uc - the user context
    route - api route copied from valence docs
    params - dictionary of parameters - keys = what to replace

    Returns :
    request result 
    '''    
    for key in params:
        route = route.replace("({})".format( key ), str(params[key]) )
    
    url = uc.create_authenticated_url(route,method='PUT')
    return requests.put(url,json=data)

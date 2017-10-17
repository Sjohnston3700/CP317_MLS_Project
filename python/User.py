from api_functions import getApiVersions
from API import ValenceAPI as API
from Course import Course

class User(object):
    '''
    Class to store Valence user context and things they have access to do.
    '''

    def __init__(self,context):
        '''
        
        '''
        self.uc = context
        self.API = API(self.uc.host,self.uc.scheme)
        self.courses = [ Course(self.uc,item,self.API) for item in self.API.getCourses(self.uc) ]
        
        

    def getCourse(self,Id):
        '''
        Function to return a specific class based on the Valence ID. 
        
        Preconditions:
            Id (int or str) : the value class Id
        
        Returns the course if it's associated with this User None if not found  
        '''
        try:
            return [ course for course in self.courses if str(course.Id) == str(Id) ][0]
        except:
            return None

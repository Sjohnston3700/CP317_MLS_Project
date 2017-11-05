from api_functions import getApiVersions
import API
from Course import Course

class User(object):
    '''
    Class to store Valence user context and things they have access to do.
    '''

    def __init__(self,context,host,roles=[]):
        '''
        
        '''
        self._context = context
        self._host = host
        self._courses = [Course(self,item) 
                        for item in API.get_user_enrollments(self)
                        if item['Access']['ClasslistRoleName'] == 'TA']
        context_info = API.get_who_am_i(self)
        self._name = '{} {}'.format(context_info['FirstName'], context_info['LastName'])
        
    def get_courses(self):
        return self._courses

    def get_course(self, id):
        '''
        Function to return a specific class based on the Valence ID. 
        
        Preconditions:
            Id (int or str) : the value class Id
        
        Returns the course if it's associated with this User None if not found  
        '''
        try:
            return [course for course in self._courses if str(course.get_id()) == str(id)][0]
        except:
            return None
    
    def get_context(self):
        return self._context
    
    def get_host(self):
        return self._host

    def get_name(self):
        return self._name

import logging
import API, Course

logger = logging.getLogger(__name__)

class User(object):
    
    def __init__(self, context, host, roles=[]):
        """
        Instantiates a new User object
        Preconditions:
            context: The Brightspace User context ()
            host: The Host object corresponding to the user (Host)
            roles: List of roles, default: [] (list)
        """
        self._context = context
        self._host = host
        
        try:
            self._json = API.get_who_am_i(self)
            self._courses = API.get_courses(self)#still need to filter by role
        except Exception as e:
            logger.error('Something went wrong. Unable to create User object.')
            raise
    
    def get_first_name(self):
        '''
        Function to return logged in users first name
        '''
        return self._json['FirstName']
    
    def get_last_name(self):
        '''
        Function to return logged in users last name
        '''
        return self._json['LastName']
    
    def get_id(self):
        '''
        Function to return loggeed in users internal Brightspace Id
        '''
        return self._json['Identifier']
    
    def get_name(self):
        '''
        Function to return logged in users first and last name
        '''
        return '{} {}'.format( self.get_first_name(), self.get_last_name() )
    
    def get_context(self):
        """
        Returns the user context belonging to this user
        
        Postconditions:
            returns
            A Brightspace user context
        """
        return self._context                

    def get_course(self, id):
        """
        Returns a single course with id matching the given id, None if this 
        User does not have access to the course
        
        Preconditions:
            id - ID of the course (str or int)
        Postconditions
            returns
            A single course object with matching id, None if this User cannot access that course
        """
        for course in self._courses:
            if str( course.get_id() ) == str( id ):
                return course
        return None        
        
    def get_courses(self):
        """
        Returns the list of courses the user has access to
        
        Postconditions:
            returns
            Copy of a python list of all courses accessible by this user
        """
        return self._courses

    def get_host(self):
        """
        Gets the host being used by this User
        
        Postconditions:
            returns 
            A Host object
        """
        return self._host


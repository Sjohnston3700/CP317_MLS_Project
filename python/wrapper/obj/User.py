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
            roles: List of roles, default: None (list)
        """
        self.context = context
        self.host = host
        
        me = API.get_who_am_i(self)
        self._name = '{} {}'.format(me['FirstName'], me['LastName'])
        self._id = me['Identifier']
        self._courses = API.get_courses(self)#still need to filter by role

    def get_context(self):
        """
        Returns the user context belonging to this user
        
        Postconditions:
            returns
            A Brightspace user context
        """
        return self.context                

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
        Returns a copy of the list of courses the user has access to
        
        Postconditions:
            returns
            Copy of a python list of all courses accessible by this user
        """
#        return copy.deepcopy(self._courses)#Deepcopy doesn't know how to deal with a list of courses
        return self._courses#need to find a way to make deepcopy happy
        #maybe https://stackoverflow.com/questions/6279305/typeerror-cannot-deepcopy-this-pattern-object

    def get_host(self):
        """
        Gets the host being used by this User
        
        Postconditions:
            returns 
            A Host object
        """
        return self.host


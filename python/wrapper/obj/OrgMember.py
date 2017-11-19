import copy
import API

class OrgMember(object):
    def __init__(self, org_member_params):
        """
        Instantiates a new OrgMember object 
        
        Preconditions:
            org_member_params: Parameters to init this user (dict)
        """
        self._id        = org_member_params['User']['Identifier']
        self._name      = org_member_params['User']['DisplayName']
        self._org_id    = org_member_params['User']['OrgDefinedId']
        self._role      = org_member_params['Role']['Id']

    def get_id(self):
        """
        Postconditions:
            returns
            The Brightspace ID of the OrgMember (str)
        """
        return self._id        
        
    def get_name(self):
        """
        Postconditions:
            returns
            The name of the OrgMember (str)
        """
        return self._name
    
    def get_org_id(self):
        """
        Postconditions:
            returns
            The organization defined ID of the OrgMember (str)
        """
        return self._org_id

    def get_role(self):
        """
        Postconditions:
            returns
            The role id of the OrgMember (str)
        """
        return self._role

from Course import Course

class User(OrgMember):
    
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
        self._courses = [Course(self,item) 
                for item in API.get_user_enrollments(self)
                if item['Role']['Name'] in roles]

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
        for course in self.courses:
            if course.get_id() == id:
                return course
        return None        
        
    def get_courses(self):
        """
        Returns a copy of the list of courses the user has access to
        
        Postconditions:
            returns
            Copy of a python list of all courses accessible by this user
        """
        return copy.deepcopy(self.courses)

    def get_host(self):
        """
        Gets the host being used by this User
        
        Postconditions:
            returns 
            A Host object
        """
        return self.host



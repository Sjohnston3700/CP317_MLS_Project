import copy
import API

class OrgMember(object):
	"""
	Instantiates a new OrgMember object 
	
	Preconditions:
		org_member_params: Parameters to init this user (dict)
	"""
    def __init__(self, org_member_params):
		
        self._name      = org_member_params['User']['DisplayName']
        self._id        = org_member_params['User']['Identifier']
        self._org_id    = org_member_params['User']['OrgDefinedId']
        self._role      = org_member_params['Role']['Id']

	"""
	Postconditions:
		returns
		The name of the OrgMember (str)
	"""
    def get_name(self):
        return self._name

	"""
	Postconditions:
		returns
		The Brightspace ID of the OrgMember (str)
	"""
    def get_id(self):
        return self._id
	
	"""
	Postconditions:
		returns
		The organization defined ID of the OrgMember (str)
	"""
    def get_org_id(self):
        return self._org_id

	"""
	Postconditions:
		returns
		The role id of the OrgMember (str)
	"""
    def get_role(self):
        return self._role


class User(OrgMember):
	"""
	Instantiates a new User object, inherits from OrgMember
	Preconditions:
		context: The Brightspace User context ()
		host: The Host object corresponding to the user (Host)
		roles: List of roles, default: None (list)
	"""
	def __init__(self, context, host, roles=None):
		self.context = context
		self.host = host
		
		# TODO: get courses we can access from roles[]
		self.courses = []
		version = API.get(API.API_ROUTE) # Get Brightspace API version
		API.get(API.GET_USER_ENROLLMENTS, self, {'version': version}) # Get user enrollments
	"""
	Returns a copy of the list of courses the user has access to
	
	Postconditions:
		returns
		Copy of a python list of all courses accessible by this user
	"""
	def get_courses(self):
		return copy.deepcopy(self.courses)

	"""
	Returns a single course with id matching the given id, None if this 
	User does not have access to the course
	
	Preconditions:
		id - ID of the course (str or int)
	Postconditions
		returns
		A single course object with matching id, None if this User cannot access that course
	"""
	def get_course(self, id):
		# Create a lambda to find the correct id in list of Course objects
		return self.courses.find(lambda x: x.get_id() == id)
	
	"""
	Returns the user context belonging to this user
	
	Postconditions:
		returns
		A Brightspace user context
	"""
	def get_context(self):
		return self.context

	"""
	Gets the host being used by this User
	
	Postconditions:
		returns 
		A Host object
	"""
	def get_host(self):
		return self.host


o = User('context', 'host', 'roles')
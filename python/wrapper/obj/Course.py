import GradeItem, OrgMember, API
import logging, copy

logger = logging.getLogger(__name__)

class Course(object):
    '''
    Class for Course
    '''
    
    def __init__(self, user, course_params):
        """
        Constructor for a Course object.
        
        Preconditions:
            user (User) : Info about user.
            course_params (dict) : Info about course (Enrollment.MyOrgUnitInfo).
        
        Postconditions:
            On success:
                Course object for user is initialized.
            On failure:
                Error message is logged and raises exception.
                
        Does not error checking to validate course_params 
        """
        self._json = course_params
        self._user = user
        try:
            self._grade_items = API.get_grade_items(self)
            self._members = API.get_class_list(self)
        except Exception as e:
            logger.error('Something went wrong. Unable to create Course object with JSON {}. {}'.format(self._json,e) )
            raise
            
    def get_json(self):
        '''
        Function to return objects JSON gets.
        
        Preconditions:
            self (Course object) : Course object instance.
            
        Postconditions:
            Returns:
            Deep copy of JSON.
        '''
        return copy.deepcopy(self._json)

    def get_grade_items(self):
        """
        Function to return all the current grade item objects (Numeric) for current course.
        
        Preconditions:
            self (Course) : Course object instance.
            
        Postconditions:
            On success:
                Returns:
                self._grade_items (list) : List of current grade items.
            On failure:
                Grade items not found, returns NameError
        """
        return self._grade_items

    def get_grade_item(self,grade_item_id):
        """
        Function to return a specific grade item object (Numeric).
        
        Preconditions:
            self (Course) : Course object instance.
            grade_item_id (int) : Id number of grade item object.
            
        Postconditions:
            On success:
                Returns:
                item (GradeItem) : GradeItem object.
            On failure:
                Grade item not found, returns NameError
        """
        for item in self._grade_items:
            if str(item.get_id() ) == str(grade_item_id):
                return item
        raise NameError('Unable to find grade_item with id = {} in course : {}'.format(grade_item_id,self.get_name() ) )
    
    def get_id(self):
        """
        Function to return the id for the current course.
        
        Preconditions:
            self (Course) : Course object instance.
            
        PostConditions:
            Returns:
            self.id (int) : Id for the current course.
        """
        return self._json['OrgUnit']['Id']   
    
    def get_name(self):
        """
        Function to return the name of course.
        
        Preconditions:
            self (Course) : Course object instance.
        
        PostConditions:
            Returns:
            self.name (str) : Current course name.
        """
        return self._json['OrgUnit']['Name']

    def get_member(self,org_id):
        """
        Function to return the member request if it exist, 
        Otherwise, returns None.
        
        Preconditions:
            self (Course) : Course object instance.
            org_id (int) : Id number of the OrgMember.
            
        Postconditions:
            On success:
                Returns:
                member (OrgMember) : OrgMember object.
            On failure:
                Returns:
                None
        """
        for member in self._members:
            if member.get_org_id() == org_id:
                return member
        return None        

    def get_members(self,role=[]):
        """
        Function to return all the users for the current course.
        
        Preconditions:
            self (Course) : Course object instance.
            role (list) : Role of user.
        
        Postconditions:
            On success:
                Returns:
                items (list) : All OrgMembers of a specific role in current Course.
                OR
                self._members : All OrgMembers in current Course.
        """
        if role != []:
            items=[]
            for member in self._members:
                if member.get_role() in role:
                    items.append(member)
            return items 
        return self._members
        
    def get_user(self):
        """
        Function will return the user object.
        
        Preconditions:
            self (Course) : Course object instance.
            
        Postconditions:
            Returns:
            self._user (User) : Current User object. 
        """
        return self._user
        
    def get_user_role(self):
        """
        Function will return the user role for current course.
        
        Preconditions:
            self (Course) : Course object instance.
            
        Postcondition:
            Returns:
            self.user_role (str) : User role for current course.
        """
        return self._json['Role']['Name']

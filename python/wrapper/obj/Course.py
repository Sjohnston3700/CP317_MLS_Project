import GradeItem, OrgMember, API
import logging

logger = logging.getLogger(__name__)

class Course(object):
    '''
    Class for Course
    '''
    
    def __init__(self,user,course_params):
        """
        user (user object) - info about user
        course_params - info about course (Enrollment.MyOrgUnitInfo)
        
        Does not error checking to validate course_params 
        """
        self._json = course_params
        self._user = user
        try:
            self._grade_items = API.get_grade_items(self)
            self._members = API.get_class_list(self)
        except Exception as e:
            logger.error('Something went wrong. Unable to create Course object with json {}. {}'.format(self._json,e) )
            raise
            
    def get_json(self):
        '''
        Function to return objects json guts
        '''
        return self._json

    def get_grade_items(self):
        """
        Function will return all the current grade object (Numeric) for current course
        return:
            Gradeitems - list
        exception:
            not find will return NameError
        """
        return self._grade_items

    def get_grade_item(self,grade_item_id):
        for item in self._grade_items:
            if str(item.get_id() ) == str(grade_item_id):
                return item
        raise NameError('Unable to find grade_item with id = {} in course : {}'.format(grade_item_id,self.get_name() ) )
    
    def get_id(self):
        """
        Function will return the id for the current course
        PostCondition:
            reutrn self.id - Id for the current course
        """
        return self._json['OrgUnit']['Id']   
    
    def get_name(self):
        """
        Function will return the name of course
        PostCondition:
            return self.name - current course name
        """
        return self._json['OrgUnit']['Name']

    def get_member(self,org_id):
        """
        Function will return the member request if it exist, 
        Otherwise, it return None
        """
        for member in self._members:
            if member.get_org_id() == org_id:
                return member
        return None        

    def get_members(self,role=[]):
        """
        Function will return all the users for the current course
        return :
            list of Orgmember
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
        Function will return the user object
        PostCondition:
            return self._user - user 
        """
        return self._user
        
    def get_user_role(self):
        """
        Function will return the user fole for current course
        PostCondition:
            reutrn self.user_role - user role for current course
        """
        return self._json['Role']['Name']

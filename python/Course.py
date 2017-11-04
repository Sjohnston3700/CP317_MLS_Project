from GradeItem import NumericGradeItem
from OrgMember import OrgMember
import API

class Course(object):
    '''
    
    '''
    
    def __init__(self,user,course_params):
        """
        user (user object) - info about user
        course_params (json) - info about course (Enrollment.MyOrgUnitInfo) 
        """
        self._name      = course_params['OrgUnit']['Name']
        self._id        = course_params['OrgUnit']['Id']
        self._user_role = course_params['Access']['ClasslistRoleName']
        self._user = user
        self._grade_items = self._get_grade_items()
        self._members = [OrgMember(member) for member in API.get_course_members(self)]

    def _get_grade_items(self):
        items = []
        for item in API.get_grade_items(self):
            if item['GradeType'] == 'Numeric':
                items.append(NumericGradeItem(self, item))
        return items

    def get_grade_items(self):
        return self._grade_items

    def get_grade_item(self,id):
        try:
            return [grade_item for grade_item in self._grade_items if str(grade_item.get_id()) == str(id)][0]
        except:
            return None
    
    def get_name(self):
        """
        Function will return the name of course
        PostCondition:
            return self.name - current course name
        """
        return self._name

    def get_id(self):
        """
        Function will return the id for the current course
        PostCondition:
            reutrn self.id - Id for the current course
    """
        return self._id

    def get_user_role(self):
        """
        Function will return the user fole for current course
        PostCondition:
            reutrn self.user_role - user role for current course
        """
        return self._user_role

    def get_members(self,role=[]):
        return self._members

    def get_member(self,org_id):
        try:
            return [member for member in self._members if str(member.get_org_id()) == str(org_id)][0]
        except:
            return None

    def get_user(self):
        """
        Function will return the user object
        PostCondition:
            return self._user - user 
        """
        return self._user
























#*****************************************************************
# OLD CODE
# # ****************************************************************************    
#     def _getGradeItems(self):
#         try:
#             grade_items = [GradeItem(self.uc,item,self.API) for item in self.API.getGradeItems(self.uc,self.Id,self.name)]
#         except Exception as e:
#             grade_items = []
#             print(str(e))
#         return grade_items
        
#     def getGradeItem(self, Id):
#         '''
#         Function to return a specific gradeItem based on the Valence ID. 
        
#         Preconditions:
#             Id (int or str) : the value class Id
        
#         Returns the gradeItem if it's associated with this Course None if not found  
#         '''
#         try:
#             return [gradeItem for gradeItem in self.grade_items if str(gradeItem.Id) == str(Id)][0]
#         except:
#             return None
   

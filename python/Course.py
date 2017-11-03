from GradeItem import GradeItem
import API

class Course(object):
    '''
    
    '''
    
    def __init__(self,user,course_params):
        """
        user (user object) - info about user
        course_params (json) - info about course (Enrollment.OrgUnitInfo) 


        """
        
        self.name = course_params["name"]
        self.id = course_params["Id"]
        self.user_role = course_params["Role"]["Name"]

        self._user = user
        

    def get_grade_items(self):

        return

    def get_grade_item(self,id):

        return
    
    def get_name(self):
        """
        Function will return the name of course
        PostCondition:
            return self.name - current course name
        """
        return self.name

    def get_id(self):
        """
        Function will return the id for the current course
        PostCondition:
            reutrn self.id - Id for the current course
    """
        return self.id

    def get_user_role(self):
        """
        Function will return the user fole for current course
        PostCondition:
            reutrn self.user_role - user role for current course
        """

        return self.user_role

    def get_members(self,role):

        return 

    def get_member(self,org_id):
        return

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
   

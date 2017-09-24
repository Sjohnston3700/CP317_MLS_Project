from GradeItem import GradeItem

class Course(object):
    '''
    
    '''
    
    def __init__(self,context,course_params,api):
        self.uc = context
        self.API = api
        self.Id     = course_params['OrgUnit']['Id']
        self.name   = course_params['OrgUnit']['Name']
        self.access = course_params['Access']['CanAccess']
        self.active = course_params['Access']['IsActive']
        self.grade_items = self._getGradeItems()
        
    def _getGradeItems(self):
        try:
            grade_items = [GradeItem(self.uc,item,self.API) for item in self.API.getGradeItems(self.uc,self.Id,self.name)]
        except Exception as e:
            grade_items = []
            print(str(e))
        return grade_items
        
    def getGradeItem(self, Id):
        '''
        Function to return a specific gradeItem based on the Valence ID. 
        
        Preconditions:
            Id (int or str) : the value class Id
        
        Returns the gradeItem if it's associated with this Course None if not found  
        '''
        try:
            return [gradeItem for gradeItem in self.grade_items if str(gradeItem.Id) == str(Id)][0]
        except:
            return None
   

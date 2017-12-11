import re, logging, copy

import API
import GradeItem

logger = logging.getLogger(__name__)

class Grade(object):
    '''
    Object to hold an actual student numeric grade with a value and public/private feedback.
    '''
    '''
    def __init__(self,userId,value,maxValue,name='',public_feedback='',private_feedback=''):

        Preconditions :
            userId (str or int) : The Value userId
            value (int)  : The grade value (asssumed numeric)
            maxValue (int)      : What the grade  is out of
            name (str) : The student name (optional - default = '')
            public_feedback (str) : The public feedback (optional - default = '')
            private_feedback (str) : The private feedback (optional - default = '')

        self.userId = userId
        self.studentName = name
        self.maxValue = maxValue
        self.value  = int(value)
        self.public_feedback  = public_feedback
        self.private_feedback = private_feedback
    '''
    
    def __init__(self, grade_item, student, comment):
        '''
        Constructor for Grade object.
        
        Preconditions:
            grade_item (GradeItem) : GradeItem object that contains the grade.
            student (OrgMember) : OrgMember object of the student that has the grade.
            comment (str) : String that contains a comment for the student's grade item.
            
        Postconditions:
            Grade object for grade item and student is initialized.
        '''
        self._json = {
                    "UserId": student.get_id(),
                    "OrgUnitId": student.get_org_id(),
#                    "DisplayedGrade": <string>,
#                    "GradeObjectIdentifier": <string:D2LID>,
#                    "GradeObjectName": <string>,
#                    "GradeObjectType": <number:GRADEOBJ_T>,
#                    "GradeObjectTypeName": <string>|null,
                    "Comments": {"Content":comment,"Type":"Text"},
                    "PrivateComments": {"Content":"", "Type":"Text"}
                    }
        self._grade_item = grade_item
        self._student = student

    def get_json(self):
        '''
        Function to return a deep copy of the JSON object.
        
        Preconditions:
            self (Grade) : Grade object instance.
            
        Postconditions:
            Returns:
                A deep copy of the JSON object for the student with respect to this GradeItem.
        '''
        return copy.deepcopy(self._json)
        
    def get_comment(self):
        ''' 
        Function to return comments for this student with respect to this GradeItem.
        
        Preconditions:
            self (Grade) : Grade object instance.
        
        Postconditions:
            Returns:
                A comment's content (str) in the JSON object for the student with respect to this GradeItem.
        '''
        return self._json['Comments']['Content']

    def get_grade_item(self):
        ''' 
        Function to return the GradeItem Object.
        
        Preconditions:
            self (Grade) : Grade object instance.
            
        Postconditions:
            Returns:
                The GradeItem object that this Grade object belongs to.
        '''
        return self._grade_item        
        
    def get_student(self):
        ''' 
        Function to return the student object (OrgMember).
        
        Preconditions:
            self (Grade) : Grade object instance.
        
        Postconditions:
            Returns:
                The OrgMember object for the student that owns this grade.
        '''
        return self._student
        
    def get_user(self):
        ''' 
        Function to return the user.
        
        Preconditions:
            self (Grade) : Grade object instance.
            
        Postconditions:
            Returns:
                The GradeItem object that contains this grade.
        '''
        return self._grade_item.get_user()

    def put_grade(self):
        '''
        Function to call the API function to update the grade.
        
        Preconditions:
            self (Grade) : Grade object instance.
            
        Postconditions:
            API put_grade function is called and the grade is updated.
        '''
        API.put_grade(self)

class NumericGrade(Grade):
    '''
    Class for NumericGrades that contains a student's numeric grade value and comment.
    '''
    
    def __init__(self, grade_item, student, comment, value):
        '''
        Constructor for a NumericGrade object.
        
        Preconditions:
            grade_item (GradeItem) : GradeItem object that contains the numeric grade.
            student (OrgMember) : OrgMember object of the student that has the grade.
            comment (str) : String that contains a comment for the student's grade item.
            value (float) : Grade student obtained on the grade item.
            
        Postconditions:
            NumericGrade object for grade item and student is initialized.
        '''
        max_value = grade_item.get_max()
        assert is_numeric(value), 'Grade value must be numeric'
        assert float(value) <= max_value or grade_item.can_exceed(), 'Grade value is greater then grade item max : {}'.format( max_value )
        assert float(value) >= 0, 'Grade value must be non-negative'
        
        super().__init__(grade_item, student, comment)
        self._json['GradeObjectType'] = 1
        self._json['PointsNumerator'] = float(value)

    def get_value(self):
        '''
        Returns value of the NumericGrade item.
        
        Preconditions:
            self (Grade) : Grade object instance.
            
        Postconditions:
            Returns:
                A float grade value in the JSON object for the student with respect to this GradeItem.
        '''
        return self._json['PointsNumerator']
        
def is_numeric(value):
    '''
    Returns a boolean to determine if a value is numeric or not.
    
    Preconditions:
        value (float) : Grade student obtained on the grade item.
        
    Postconditions:
        Returns:
            True if value is numeric or false if not.
    '''
    try:
        float(value)
        return True
    except:
        return False

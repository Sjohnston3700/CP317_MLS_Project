import re,sys

FEEDBACK_PATTERN = '\-{3,}?.*?(\d{5,7}).*?^([\w|\s]*?)$(.+?(?:Total:\s+(\d+)\s+\/\s+(\d+).*?)?)\-{3,}?'

class Grade(object):
    '''
    Object to hold an actual student numeric grade with a value and public/private feedback
    
    '''
    '''def __init__(self,userId,value,maxValue,name='',public_feedback='',private_feedback=''):
    
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
        self.private_feedback = private_feedback'''

    def upload_grade():
        return

    def get_comment():
        return self.comment

    def get_user():
        return object.student

    def get_grade_item():
        return object.grade_item

    def get_student():
        return object.student


class NumericGrade():
    """
    -----------------------------------------------------
    Constructor
    -----------------------------------------------------
    Precondition:
        - grade_item (GradeItem)
        - student (OrgMember)
        - grade_param (JSON)
    Postcondition:
        - Create object with attributes
    -----------------------------------------------------
    """
    def __init__(self, grade_item, student, grade_param):
        super(Grade,self).__init__
        self.grade_item = grade_item
        self.student = student
        self.grade_param = grade_param

    def get_value():
        return self.value





    
   

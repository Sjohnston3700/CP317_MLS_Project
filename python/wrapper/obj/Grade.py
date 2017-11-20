import re, logging

import API
import GradeItem

FEEDBACK_PATTERN = '\-{3,}?.*?(\d{5,7}).*?^([\w|\s]*?)$(.+?(?:Total:\s+(\d+)\s+\/\s+(\d+).*?)?)\-{3,}?'

logger = logging.getLogger(__name__)

class Grade(object):
    '''
    Object to hold an actual student numeric grade with a value and public/private feedback

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
        """
        Constructor:
            grade_item(GradeItem Object)
            student(OrgMember)
            comment (String)
        """
        self._grade_item = grade_item
        self._student = student
        self._comment = comment

    def get_comment(self):
        ''' Return comments for this student with respect to this GradeItem '''
        return self._comment

    def get_grade_item(self):
        ''' Return the GradeItem Object '''
        return self._grade_item        
        
    def get_student(self):
        ''' Return the student object (OrgMember) '''
        return self._student
        
    def get_user(self):
        ''' Return the user '''
        return self._grade_item.get_user()

    def put_grade(self):
        '''Call function to update grade '''
        API.put_grade(self)

class NumericGrade(Grade):

    def __init__(self, grade_item, student, comment, value):
        """
        Constructor:
            grade_item(GradeItem Object)
            student(OrgMember)
            comment(feedbacks) string
            value(mark student scored) float
        """
        super().__init__(grade_item, student, comment)
        self._value = value

    def get_value(self):
        '''Returns value of the NumericGrade Item '''
        return self._value

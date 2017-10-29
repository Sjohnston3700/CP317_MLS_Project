import re,sys

FEEDBACK_PATTERN = '\-{3,}?.*?(\d{5,7}).*?^([\w|\s]*?)$(.+?(?:Total:\s+(\d+)\s+\/\s+(\d+).*?)?)\-{3,}?'

class Grade(object):
    '''
    Object to hold an actual student numeric grade with a value and public/private feedback
    
    '''
    def __init__(self,userId,value,maxValue,name='',public_feedback='',private_feedback=''):
        '''
        Preconditions :
            userId (str or int) : The Value userId 
            value (int)  : The grade value (asssumed numeric)
            maxValue (int)      : What the grade  is out of 
            name (str) : The student name (optional - default = '')
            public_feedback (str) : The public feedback (optional - default = '')
            private_feedback (str) : The private feedback (optional - default = '')
        '''
        self.userId = userId
        self.studentName = name
        self.maxValue = maxValue
        self.value  = int(value)
        self.public_feedback  = public_feedback
        self.private_feedback = private_feedback
    
   
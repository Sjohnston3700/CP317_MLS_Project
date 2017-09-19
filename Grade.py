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
    
    
def parse_grades( grades_text ):
    '''
    Function to turn a raw string of user formatted grades into a list of Grade Items
    
    Preconditions:
        grades_text (str) : The raw string to parse
    Postconditions:
        Returns a list of Grade Objects
        
    Expected Format :
    #----------------------------------------#
    userID (int)
    User Name
    Feedback (multiline preformatted)
    Total: x(int) / y(int)

    #----------------------------------------#
    Next userId etc
    '''
    grades = []
    all_feedback = re.findall(FEEDBACK_PATTERN, grades_text, re.DOTALL|re.MULTILINE)
    for feedback in all_feedback:
        student_name = feedback[1].strip()
        studentId = feedback[0].strip()
        public_feedback = feedback[2]
        grade_value = feedback[3] if feedback[3] != '' else '0'
        out_of       = feedback[4] if feedback[4] != '' else 0 
		
        grade = Grade(studentId,grade_value,out_of,student_name,public_feedback)
        grades.append(grade)
		
    return grades
    

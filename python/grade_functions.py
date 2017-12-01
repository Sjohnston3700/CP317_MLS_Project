import csv # To handle csv files
import re,sys

from wrapper.obj.API import get as getRoute, put as putRoute
from wrapper.obj.Grade import Grade
from io import TextIOWrapper # To check if file object is valid

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

def parse_grades_csv( csv_file ):
    '''
    Parses Grade objects from a CSV file in the format
        student_name, mls_id, grade, comment
    Note: If csv is not opened in binary mode, errors may occur
    Preconditions:
        csv_file - The csv file to read from (file must be opened with 'r')
    Postconditions:
        returns
        grades    - A list of json dictionary values corresponding to each line of the file
        or errors - A list of json dictionary values corresponding to issues with the file
    '''
    assert isinstance(csv_file, TextIOWrapper), "CSV file must be opened with 'r'"  # Check if csv is an instance of a file object
    grades = []
    errors = []
    try:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for line_number, line in enumerate(reader):
            # unescape any escaped characters read by csv.reader
            if len(line) < 4:
                errors.append( {'line':line_number+1,'msg':'Format must be brightspace_id, grade, student_name, comment'} )
            else:
                comment = line[3]
                for before, after in {'\\n':'\n', '\\r':'\r', '\\t':'\t', '\\"': '"', "\\'":"'"}:
                    comment = comment.replace(before, after)
                #              ID         value         name     comment
                keys = ['id','value','name','comment']
                grade = {}
                for index, key in enumerate(keys):
                    grade[key]= line[index]
            
                grades.append( grade )
    except Exception as e:
        print(e)
        errors = [{'msg' : 'Entire file is formatted incorrectly. Please ensure each student entry is formatted as student_name, brightspace_id, grade, comment'}]
    
    if len(errors) != 0:
        return errors
    else:
        return grades


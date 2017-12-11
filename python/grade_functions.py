import csv # To handle csv files
import re,sys, traceback

from wrapper.obj.API import get as getRoute, put as putRoute
from wrapper.obj.Grade import Grade, NumericGrade
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
        if len(grades) == 0:
            raise Exception('File is empty')        
    except Exception as e:
        errors = [{'msg' : 'Entire file is formatted incorrectly. Please ensure each student entry is formatted as student_name, brightspace_id, grade, comment'}]
    
    if len(errors) != 0:
        return errors
    else:
        return grades

def check_grades(grades_json, grade_item):
    '''
    Function to check if submitted grades are valid.
    
    Preconditions:
        grades_json (list of json grades) : The grades to validate
        grade_item (GradeItem) : The gradeitem these grades are associated with
        
    Postconditions:
        errors (list of json formatted errors )  : The grades that are invalid and the associated error
        valid_grades (list to of grade objects ) : The grades that were valid
    '''
    valid_grades = []
    errors = []
    fail_errors = []
    line = 0
    
    course = grade_item.get_course()
    for grade_json in grades_json:
        try:
            student_id  = grade_json['id']
            grade_value = grade_json['value']
            comment     = grade_json['comment']
        except Exception as e:
            error = grade_json
            error['msg']  = str(e)
            error['type'] = 1
            error['line'] = str(line)
            errors.append(error)
            line += 1
            continue   
        
        student = course.get_member(student_id)
        #student doesn't exist
        if student is None:
            error = grade_json
            error['msg'] = 'Student {} not found for course'.format(grade_json['name'])
            error['type'] = 2
            error['line'] = str(line)
            fail_errors.append(error)
            line += 1
            continue
        print('here')
        try:
            numberTest = float(grade_json['value'])
        except Exception as e:
            #not numeric
            error = grade_json
            error['msg']  = 'Grade must be an number'
            error['type'] = 1
            error['line'] = str(line)
            errors.append(error)
            line +=1 
            continue
        if float(grade_json['value']) < 0:
            error = grade_json
            error['msg']  = 'Grade cannot be negative'
            error['type'] = 1
            error['line'] = str(line)
            errors.append(error)
        elif (float(grade_json['value']) > grade_item.get_max() and not grade_item.can_exceed()):
            error = grade_json
            error['msg']  = 'Grade is more than the grade maximum'
            error['type'] = 1
            error['line'] = str(line)
            errors.append(error)
        else:
            print('past max check')
            try:
                print('sending away')
                grade = NumericGrade(grade_item, student, comment, grade_value)        
                valid_grades.append(grade)
            except Exception as e:
                error = grade_json
                error['msg']  = str(e)
                error['type'] = 1
                error['line'] = str(line)
                errors.append(error)
        line += 1
    
    if fail_errors != []:
        errors = fail_errors
        
    return errors, valid_grades

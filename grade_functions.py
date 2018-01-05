import csv # To handle csv files
import re,sys, traceback
from app import app

from wrapper.obj.API import get as getRoute, put as putRoute, put_grade
from wrapper.obj.Grade import Grade, NumericGrade
from io import TextIOWrapper # To check if file object is valid


def parse_grades( csv_file ):
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
                if len(line) == 0:
                    errors.append({'line': line_number+1, 'msg':''})
                else:
                    errors.append({'line': line_number+1, 'msg':line})
            
            elif line[0]=='' or line[1]=='' or line[2]=='':
                errors.append({'line':line_number+1, 'msg':line})
            
            else:
                comment = line[3]
                for before, after in {'\\n':'\n', '\\r':'\r', '\\t':'\t', '\\"': '"', "\\'":"'"}:
                    comment = comment.replace(before, after)
                #              ID         value         name     comment
                keys = ['id','value','name','comment']
                grade = {}
                for index, key in enumerate(keys):
                    grade[key] = line[index]
            
                grades.append( grade )
        if len(grades) == 0 and len(errors) == 0:
            errors=[{'msg':'Empty file submitted'}]
        elif len(grades) == 0:
            raise Exception
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
        
        student = course.get_member(brightspace_id=student_id)
        #student doesn't exist
        if student is None or student.get_role() != 101:
            error = grade_json
            error['msg'] = 'Student {} not found in course'.format(grade_json['name'])
            error['type'] = 2
            error['line'] = str(line)
            fail_errors.append(error)
            line += 1
            continue
        try:
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
    
def upload_grades_function(grades, user, course, grade_item):
    '''
    Function to upload grades to Brightspace.
    Preconditions:
        grades (dict)          : json information for each grade being checked.
        course (Course)        : Course that the grades belong to.
        grade_item (GradeItem) : GradeItem that the grade belong to.
    Postconditions:
        errors (list of json formatted errors ) : The grades that are invalid and the associated error. not quite implemented.   
    '''    
    errors=[]
    successful_grades=[]
    for grade in grades:
        id = grade['id']
        student = course.get_member(brightspace_id=id)
        grade = NumericGrade(grade_item, student, grade['comment'], grade['value'])
        
        #if no errors, add to successful_id
        if not put_grade(grade):
            successful_grades.append(grade)
        
    if errors==[] or type(errors[0]==float):
        report = {'total':len(grades), 'successful': len(successful_grades), 'grades':successful_grades}
        key = '{}_report'.format(user.get_id() )
        app.config[key] = report
    else:
        key = '{}_report'.format(user.get_id() )
        app.config[key] = {'errors': errors}
    
    return errors
    
    

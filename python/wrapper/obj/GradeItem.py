import logging
import API, Grade

logger = logging.getLogger(__name__)

class GradeItem(object):
    
    def __init__(self, course, grade_item_params):
        """
        Preconditions:
            course (Course object) - the course the GradeItem is for
            grade_item_params (json) - info about GradeItem  
            
        Postconditions:
            parent constructor to all GradeItem types. contains data common to all types
        """
        if type(self) == GradeItem:
            raise TypeError("GradeItem must be subclassed")
        self._name = grade_item_params['Name']
        self._id = grade_item_params['Id']
        self._course = course
        self._grades = []

    def get_course(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._course - Course that the GradeItem belongs to
        """
        return self._course

    def get_grade(self, student):
        """
        Gets grade for a given student
        Preconditions:
            student: OrgMember -> student whose grade we are looking for
        Postconditions:
            Returns: Grade object if there is a grade belonging to the student
                     Returns None if student grqade is not found
        """
        for grade in self._grades:
            if (student.get_id() == grade.get_student().get_id()):
                return grade
        return None

    def get_grades(self):
        """
        Getter function
        Postconditions:
            Returns: List of Grade objects associated with this GradeItem
        """
        return self._grades

    def get_id(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._id - Id of the GradeItem
        """
        return self._id
        
    def get_name(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._name - name of the GradeItem
        """
        return self._name

    def get_user(self):
        """ 
        Getter function
        Postconditions:
            Returns: User object - User associated with the GradeItem
        """
        self._course.get_user()
        
    def put_grade_item(self):
        """
        Puts grade item to Brightspace
        """
        raise NotImplementedError('Abstract method not implemented.')
        
    def put_grades(self):
        """
        Calls grade.put_grade() for each Grade object
        """
        for grade in self._grades:
            grade.put_grade()
        return

class NumericGradeItem(GradeItem):
    def __init__(self, course, grade_item_params):
        """
        Preconditions:
            course (Course object) - the course the NumericGradeItem is for
            grade_item_params (json) - info about GradeItem (Grade.GradeObject: GradeType must be numeric!) 
            
        Postconditions:
            creates object of type NumericGradeItem
        """
        if grade_item_params['GradeType'] != 'Numeric':
            raise Exception('GradeType for GradeItem {} of Course {} is not numeric.'.format(grade_item_params['Id'], course.get_id()))
        super().__init__(course, grade_item_params)                      
        self._max_points = grade_item_params['MaxPoints']
        self._can_exceed_max_points = grade_item_params['CanExceedMaxPoints']

    def can_exceed(self):
        """
        Getter function
        Postconditions:
            returns: self._get_can_exceed
        """
        return self._can_exceed_max_points        
    
    def create_grade(self, student, grade_params):
        """
        Creates a NumericGrade object and adds to the list (Called by ezMarker)
        Preconditions:
            student: OrgMember object
            grade_params: Python dictionary of parameters required to initialize a NumericGrade
        """
        self._grades.append(NumericGrade(self, student, grade_params))
        return
    
    def get_max(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._max_points - The max number of points this GradeItem can have for any one Grade ?? I think
        """
        return self._max_points
     
    def put_grade_item(self, params):
        """
        PLACEHOLDER - Until attributes get figured out
        """
        API.put_grade_item(self)
        return
        
    def within_max(self, value):
        """
        Checks if a value is within below the max points of the grade object
        preconditions:
            value: the value to check against max_points
        Postconditions:
            Returns: Boolean - false if not value larger than maxa points 
        """
        
        return (value <= self._max_points)
        

    

    
        
        

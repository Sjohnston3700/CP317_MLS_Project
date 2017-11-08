class GradeItem(object):
    
    def __init__(self, course, grade_item_params):
        """
        Preconditions:
            course (Course object) - the course the GradeItem is for
            grade_item_params (json) - info about GradeItem  
            
        Postconditions:
            parent constructor to all GradeItem types. contains data common to all types
        """
        if type(this) == GradeItem:
            raise TypeError("GradeItem must be subclassed")
        this._name = grade_item_params['Name']
        self._id = grade_item_params['Id']
        this._course = course

    def get_name(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._name - name of the GradeItem
        """
        return self._name

    def get_id(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._id - Id of the GradeItem
        """
        return self._id
       
    def get_user(self):
        """ 
        Getter function
        Postconditions:
            Returns: User object - User associated with the GradeItem
        """
        self._course.get_user()
        
    def get_course(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._course - Course that the GradeItem belongs to
        """
        return self._course
 
    def get_grade(self, student):
        raise NotImplementedError

    def upload_grades(self):
        raise NotImplementedError

    def put_grade_item(self, params):
        raise NotImplementedError

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
    
    def create_grade(self, student, grade_params):
        raise NotImplementedError
    
    def get_max(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._max_points - The max number of points this GradeItem can have for any one Grade ?? I think
        """
        return self._max_points
    

    

    
        
        

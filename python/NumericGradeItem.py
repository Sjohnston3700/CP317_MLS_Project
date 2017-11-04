from GradeItem import GradeItem

class NumericGradeItem(GradeItem):
    def __init__(self, course, grade_item_params):
        """
        course (Course object) - the course the NumericGradeItem is for
        grade_item_params (json) - info about GradeItem (Grade.GradeObject: GradeType must be numeric!) 
        """
        if grade_item_params['GradeType'] != 'Numeric':
            raise Exception('GradeType for GradeItem {} of Course {} is not numeric.'
                                .format(grade_item_params['Id'], course.get_id()))

        self._course = course
        self._user = course.get_user()
        self._name       = grade_item_params['Name']
        self._id         = grade_item_params['Id']
        self._max_points = grade_item_params['MaxPoints']

    def get_name(self):
        return self._name
    
    def get_id(self):
        return self._id

    def get_user(self):
        return self._user

    def get_course(self):
        return self._course
    
    def create_grade(self, student, grade_params):
        raise NotImplementedError
    
    def get_max(self):
        return self._max_points
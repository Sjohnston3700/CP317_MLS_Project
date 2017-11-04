class GradeItem(object):
    def __init__(self):
        raise NotImplementedError("Implement this in the subclass.")

    def get_name(self):
        raise NotImplementedError("Implement this in the subclass.")
    
    def get_id(self):
        raise NotImplementedError("Implement this in the subclass.")

    def get_user(self):
        raise NotImplementedError("Implement this in the subclass.")

    def get_course(self):
        raise NotImplementedError("Implement this in the subclass.")
    
    def get_grade(self, student):
        raise NotImplementedError

    def upload_grades(self):
        raise NotImplementedError

    def put_grade_item(self, params):
        raise NotImplementedError

    

    

    
        
        

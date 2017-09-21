class GradeItem(object):
    '''
    
    '''
    
    def __init__(self,context,gradeItem_parameters,api):
        self.uc   = context
        self.API  = api
        self.name      = gradeItem_parameters['Name']
        self.Id        = gradeItem_parameters['Id']
        self.type      = gradeItem_parameters['GradeType']
        self.maxPoints = float(gradeItem_parameters['MaxPoints']) if self.type == 'Numeric' else None
        
    
    def setUserGrade(self, userId,courseId,gradeValue,PublicFeedback='',PrivateFeedback=''):
        '''
        Function set the grade for this grade item for a given user.
        Only works for numeric grades
        
        Preconditions:
            userId (int or str)   : The user ValenceId
            CourseId (int or str) : The course Id number 
            gradeValue (int)      : The user grade ( <= self.maxPoints )
            PublicFeedback (formatted string)  : Any feedback for the user (default is "")
            PrivateFeedback (formatted string) : Any feedback for the markers (default is "")
        Postconditions :
            Returns None on success or fails with an RuntimeError or assertion if the grade is invalid
        '''
        assert gradeValue <= self.maxPoints, 'Grade Value {} is > Max Points ({}) for {}'.format(gradeValue, self.maxPoints,self.name)
        PublicFeedback  = '<pre>{}</pre>'.format(PublicFeedback)
        PrivateFeedback = '<pre>{}</pre>'.format(PrivateFeedback)
        
        grade_data = {"Comments": { "Content": PublicFeedback, "Type": "Html" }, "PrivateComments": { "Content": PrivateFeedback, "Type": "Html" }, "GradeObjectType": 1, "PointsNumerator":gradeValue}
        self.API.setGrade(self.uc,userId,courseId,self.Id,grade_data)
        
        return
        

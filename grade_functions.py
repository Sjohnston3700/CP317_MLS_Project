from api_functions import getRoute,putRoute

gradeItemsRoute = '/d2l/api/le/(version)/(orgUnitId)/grades/'
gradeItemRoute  = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)'
setGradeRoute   = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)'
gradeItemKeys = ['Name','MaxPoints','Id']#List of items to extract from each grade item
grade_json = {"Comments": { "Content": "Test comment", "Type": "Text" }, "PrivateComments": { "Content": "Test Private Comment", "Type": "Text" }, "GradeObjectType": 1, "PointsNumerator": 23}

def getGradeItems(uc,courseId,apiVersion=1.22):
    '''
    Function to return a list of grade items in the course identified by courseID
    Fails  with an RuntimeError Exception if something goes wrong

    Preconditions:
    uc (api user context) : The api user context to make the call with
    courseId (str or int) : The Id of the course we're getting grade items from
    apiVersion (float) : The api Version to use (default = 1.22)
    
    Postconditions:
    Returns a list of grade items associated with this course. 
    
    '''
    results = None
    r = getRoute(uc, gradeItemsRoute,{'version':apiVersion,'orgUnitId':courseId})

    if r.status_code != 200:
        raise RuntimeError('Failed to get grade items. Request returned status code : {}, text : {}'.format(r.status_code,r.text) )
    else:
        results = []
        for result in r.json():
            grade = {}
            for key in gradeItemKeys:
                grade[key] = result[key]
            results.append(grade)
    return results


def setGradeItems(uc,courseId,gradeId,newGrades,apiVersion=1.22):
    '''
    Function to set the grades for a specific grade item. Assumes they are numeric grades
    Throws a RuntimeError Exception if something goes wrong.

    Preconditions:
    uc (api user context) : The api user context to make the call with
    courseId (str or int) : The Id of the course we're setting the grade item for
    gradeId (str or int)  : The Id of the grade Item we're setting
    newGrades ( list of dictionary itens ) : The new grades to set (eg. [{'ValenceId':studentValenceId,'Grade':gradevalue,'Comments':student_feedback,'PrivateComments':optionalFeedbackForMarkers}]
    apiVersion (float) : The api Version to use (default = 1.22)
    
    Postconditions:
    Returns status code
    '''
    
    #Get grade item to make sure the values are correct
    grade_request = getRoute(uc, gradeItemRoute,{'version':apiVersion,'orgUnitId':courseId,'gradeObjectId':gradeId})
    if grade_request.status_code != 200:
        raise RuntimeError('Failed to get grade item. Request returned status code : {}, text : {}'.format(r.status_code,r.text) )
    else:
        for new_grade in newGrades:
            gradeInfo = grade_json
            gradeInfo["Comments"]["Content"]        = new_grade["Comments"]
            gradeInfo['PrivateComments']["Content"] = new_grade['PrivateComments'] if 'PrivateComments' in new_grade else ""
            gradeInfo["PointsNumerator"] = new_grade["Grade"]

            grade_put = putRoute(uc, setGradeRoute,{'version':apiVersion,'orgUnitId':courseId,'gradeObjectId':gradeId,'userId':new_grade["ValenceId"]},gradeInfo )
            if grade_put.status_code != 200:
                raise RuntimeError('Failed to set grade for {}. Request returned status code : {}, text : {}'.format(new_grade["ValenceId"],grade_put.status_code,grade_put.text) )
    
    return

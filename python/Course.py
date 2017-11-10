from GradeItem import NumericGradeItem
from OrgMember import OrgMember
import API

GET_GRADE_ITEMS = "/d2l/api/le/(version)/(orgUnitId)/grades/"
GET_MEMBERS = "/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/"

class Course(object):
    '''
    
    '''
    
    def __init__(self,user,course_params):
        """
        user (user object) - info about user
        course_params - info about course (Enrollment.MyOrgUnitInfo) 
        """
        self._name      = course_params['OrgUnit']['Name']
        self._id        = course_params['OrgUnit']['Id']
        self._user_role = course_params['Access']['ClasslistRoleName']
        self._user = user
        self._grade_items = self._get_grade_items()
        self._members = [OrgMember(member) for member in API.get(GET_MEMBERS,user,{'version':self._user().get_host().get_api_version(),'orgUnitID':self._id})['Items']]

    def _get_grade_items(self):
        """
        Function will return list of grade items
        return :
                lists - grade item
        """
        gradeitems = API.get(GET_GRADE_ITEMS,self._user,{'version':self._user().get_host().get_api_version(),'orgUnitID':self._id})
        items = []
        for item in gradeitems:
            if item['GradeType'] == 'Numeric':
                items.append(NumericGradeItem(self, item))
        return items

    def get_grade_items(self):
        """
        Function will return all the current grade object (Numeric) for current course
        return:
            Gradeitems - list
        """
        return self._grade_items

    def get_grade_item(self,id):
        try:
            return [grade_item for grade_item in self._grade_items if str(grade_item.get_id()) == str(id)][0]
        except:
            return None
    
    def get_name(self):
        """
        Function will return the name of course
        PostCondition:
            return self.name - current course name
        """
        return self._name

    def get_id(self):
        """
        Function will return the id for the current course
        PostCondition:
            reutrn self.id - Id for the current course
    """
        return self._id

    def get_user_role(self):
        """
        Function will return the user fole for current course
        PostCondition:
            reutrn self.user_role - user role for current course
        """
        return self._user_role


    def get_members(self,role=[]):
        """
        Function will return all the users for the current course
        return :
            list of Orgmember
        """
        if role != []:
            items=[]
            for member in self._members:
                if member.get_role() in role:
                    items.append(member)
            return items 
        return self._members

    def get_member(self,org_id):
        """
        Function will return the member request if it exist, 
        Otherwise, it return None
        """
        for member in self._members:
            if member.get_org_id() == org_id:
                return member
        return None

    def get_user(self):
        """
        Function will return the user object
        PostCondition:
            return self._user - user 
        """
        return self._user

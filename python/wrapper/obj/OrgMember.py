import copy, logging

logger = logging.getLogger(__name__)

class OrgMember(object):
    def __init__(self, org_member_params):
        """
        Instantiates a new OrgMember object 
        
        Preconditions:
            org_member_params: Parameters to init this user (Enrollment.OrgUnitUser http://docs.valence.desire2learn.com/res/enroll.html#Enrollment.OrgUnitUser)
        
        Does no error checking of input    
        """
        self._data = org_member_params

    def get_id(self):
        """
        Postconditions:
            returns
            The Brightspace ID of the OrgMember (str)
        """
        return self._data['User']['Identifier']
        
    def get_name(self):
        """
        Postconditions:
            returns
            The name of the OrgMember (str)
        """
        return self._data['User']['DisplayName']
    
    def get_org_id(self):
        """
        Postconditions:
            returns
            The organization defined ID of the OrgMember (str)
        """
        return self._data['User']['OrgDefinedId']

    def get_role(self):
        """
        Postconditions:
            returns
            The role id of the OrgMember (str)
        """
        return self._data['Role']['Name']




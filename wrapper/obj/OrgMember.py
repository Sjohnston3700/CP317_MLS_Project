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
        self._json = org_member_params

    def get_json(self):
        '''
        Function to return a copy of the objects json guts
        '''
        return copy.deepcopy(self._json)
    
    def get_id(self):
        """
        Postconditions:
            returns the Brightspace ID of the OrgMember (str)
        """
        return self._json['User']['Identifier']
        
    def get_name(self):
        """
        Postconditions:
            returns the name of the OrgMember (str)
        """
        return self._json['User']['DisplayName']
    
    def get_org_id(self):
        """
        Postconditions:
            returns the organization defined ID of the OrgMember (str)
        """
        return self._json['User']['OrgDefinedId']

    def get_role(self):
        """
        Postconditions:
            returns the role id of the OrgMember (str)
        """
        return self._json['Role']['Id']




import copy, logging

logger = logging.getLogger(__name__)

class OrgMember(object):
    def __init__(self, org_member_params):
        """
        Instantiates a new OrgMember object 
        
        Preconditions:
            org_member_params: Parameters to init this user (dict)
        """
        self._id        = org_member_params['User']['Identifier']
        self._name      = org_member_params['User']['DisplayName']
        self._org_id    = org_member_params['User']['OrgDefinedId']
        self._role      = org_member_params['Role']['Id']

    def get_id(self):
        """
        Postconditions:
            returns
            The Brightspace ID of the OrgMember (str)
        """
        return self._id        
        
    def get_name(self):
        """
        Postconditions:
            returns
            The name of the OrgMember (str)
        """
        return self._name
    
    def get_org_id(self):
        """
        Postconditions:
            returns
            The organization defined ID of the OrgMember (str)
        """
        return self._org_id

    def get_role(self):
        """
        Postconditions:
            returns
            The role id of the OrgMember (str)
        """
        return self._role




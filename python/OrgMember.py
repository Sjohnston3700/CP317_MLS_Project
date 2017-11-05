class OrgMember(object):
    def __init__(self, org_member_params):
        self._name      = org_member_params['User']['DisplayName']
        self._id        = org_member_params['User']['Identifier']
        self._org_id    = org_member_params['User']['OrgDefinedId']
        self._role      = org_member_params['Role']['Id']
    
    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_org_id(self):
        return self._org_id

    def get_role(self):
        return self._role
import API

class Host(object):
    """
    Host class
    """
    def __init__(self, lms_host, protocol="http", versions=None):
        self._lms_host = lms_host
        self._protocol = protocol
        if versions is None:
            self._versions = API.get_api_versions(self)
        else:
            self._versions = versions

    def get_protocol(self):
        return self._protocol
    
    def get_lms_host(self):
        return self._lms_host

    def get_api_version(self, product_code):
        return [item['LatestVersion'] for item in self._versions if item['ProductCode'] == product_code][0]

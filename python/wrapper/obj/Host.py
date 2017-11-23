import logging
import API

logger = logging.getLogger(__name__)

class Host(object):
    """
    Host class
    """
    def __init__(self, lms_host, protocol="http", versions):
        """
            Constructor for Host Class
            
            Preconditions: 
                lms_host - hostname for the back-end LMS
                protocol - protocol to use for user <--> web-app interaction
                versions - Dictionary containing the latest versions of various products (needed for majority API calls)
            
            Postconditions:
                returns: Object of type Host
        """
        self._lms_host = lms_host
        self._protocol = protocol
        else:
            self._versions = versions
        
    def get_api_version(self, product_code):
        """ 
        Getter function
        Preconditions:
            product_code: String - product code
        Postconditions:
            Returns: LatestVersion for specific product_code
        """
        return [item['LatestVersion'] for item in self._versions if item['ProductCode'] == product_code][0]

    def get_lms_host(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._lm_host - hostname for back-end LMS
        """
        return self._lms_host        
    
    def get_protocol(self):
        """ 
        Getter function
        Postconditions:
            Returns: self._protocol - protocol used
        """
        return self._protocol
    




<?php 

include ("API.php");

class Host{ 

	function __construct($lms_host, $protocol="http", $versions=NULL) {
		/*
		Constructor for Host Class
		
		Preconditions: 
			lms_host - hostname for the back-end LMS
			protocol - protocol to use for user <--> web-app interaction
			versions - Dictionary containing the latest versions of various products (needed for majority API calls)
		
		Postconditions:
			returns: Object of type Host
        */
		
		$this->_lms_host = $lms_host;
		$this->_protocol = $protocol;

		if ($versions == NULL) {
			$this->versions = API.get_api_versions();
		} else {
			$this->versions = $versions;			
		}

   }
   
   function get_protocol() {
	   /* 
        Getter function
        Postconditions:
            Returns: self._protocol - protocol used
        */

        return $this->_protocol;
    }  
	
	function get_lms_host() { 
		/*
		Getter function
		Postconditions:
			Returns: self._lm_host - hostname for back-end LMS
		*/

        return $this->_lms_host;
    }  
	function get_api_version($product_code) {
		/* 
        Getter function
        Preconditions:
            product_code: String - product code
        Postconditions:
            Returns: LatestVersion for specific product_code
        */
		
        return [$item['LatestVersion'] foreach $this->versions as $item if($item['ProductCode'] == $product_code)][0];
    }  
	
} 

?> 
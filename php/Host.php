<?php 

// To instantiate an object use: 
// $user = User::create()->with_id(some_id); 
// To use getters: 
// $name = $user->get_name();
// To use setters: 
// $user->set_name('John Doe');

class Host(object)
{
    
    public static function create($lms_host, $protocol = "http", $versions = None)
	        /*
            Constructor for Host Class
            
            Preconditions: 
                lms_host - hostname for the back-end LMS
                protocol - protocol to use for user <--> web-app interaction
                versions - Dictionary containing the latest versions of various products (needed for majority API calls)
            
            Postconditions:
                returns: Object of type Host
			*/
    {
        
		
		
		$instance = new self();
        return $instance;
    }
    
    public function with_id($id)
    {
	  
        $this
        
        return $this;
    }
	
    public function get_name()
    {
        return $this->my_name;
    }
	
	public function set_name($new_name)
    {
        $this->my_name = $new_name;
    }
	
}

?>
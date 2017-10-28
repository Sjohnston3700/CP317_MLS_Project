<?php 

// To instantiate an object use: 
// $user = User::create()->with_id(some_id); 
// To use getters: 
// $name = $user->get_name();
// To use setters: 
// $user->set_name('John Doe');

class User
{
    
    public static function create()
    {
        $instance = new self();
        return $instance;
    }
    
    public function with_id($id)
    {
	  
        $this->my_name = 'Sarah Johnston';
        
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
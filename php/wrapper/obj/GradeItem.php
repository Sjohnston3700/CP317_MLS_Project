<?php
require_once "Grade.php";
require_once "API.php";
require_once 'OrgMember.php';

class GradeItem {
    protected $json;
    private $course;
    private $grades;

	/*
        Preconditions:
            $course (Course object) - the course the GradeItem is for
            $grade_item_params (json) - info about GradeItem  
            
        Postconditions:
            parent constructor to all GradeItem types. contains data common to all types
        */
	
	public function __construct($course, $grade_item_params){

        if (!is_subclass_of($this, 'GradeItem')) {
			throw new Exception('GradeItem must be subclassed');
		}

        $this->json = $grade_item_params;
        $this->course = $course;
        $this->grades = array();
    }
    
    function get_json() {
        return $this->json;
    }

	/*
        Getter function
	
        Postconditions:
            Returns: $this->name - name of the GradeItem
        */
	function get_name(){
		return $this->json['Name'];
	}
	
	/*
        Getter function
        
	Postconditions:
            Returns: $this->id - Id of the GradeItem
	*/
	function get_id(){
        return $this->json['Id'];
    }
	
    /*
    Getter function
    
    Postconditions:
            Returns: List of Grade objects associated with this GradeItem
    */
    function get_grades(){
        return $this->grades;
    }    
	
    /*
    Gets grade for a given student

    Preconditions:
        $student: OrgMember -> student whose grade we are looking for        
    
    Postconditions:
            Returns: Grade object if there is a grade belonging to the student
                     Returns None if student grqade is not found
     */
    function get_grade($student){
	
        foreach($this->grades as $grade){
            if ($student->get_id() == $grade->get_student()->get_id()){
                return $grade;
			}
		}
        return null; 
	}
	
    /*
    Calls $grade->put_grade() for each Grade object
    */	
    function put_grades(){
        
        foreach ($this->grades as $grade){
            $grade->put_grade();
		}
        return;
	}
		
    /*
    Puts grade item to Brightspace
    */
    function put_grade_item(){
        put_grade_item($this);
        return;
    }    
	
     /*
     Getter function
     
     Postconditions:
        Returns: User object - User associated with the GradeItem
     */
    function get_user(){
        return ($this->course->get_user());
	}
	
   /* 
   Getter function
   
   Postconditions:
       Returns: $this->course - Course that the GradeItem belongs to
    */
    function get_course(){
        return $this->course;
	}
}
class NumericGradeItem extends GradeItem {
	/*
        Preconditions:
            $course (Course object) - the course the NumericGradeItem is for
            $grade_item_params (json) - info about GradeItem (Grade.GradeObject: GradeType must be numeric!) 
            
        Postconditions:
            creates object of type NumericGradeItem
        */
	public function __construct($course, $grade_item_params){
	
		
		if ($grade_item_params["GradeType"] != "Numeric") {
			$course_id = $course->get_id();
			$the_grade_item = $grade_item_params["Id"];
            throw new RuntimeException("GradeType for GradeItem " . $course_id . "of Course " . $the_grade_item . " is not numeric.");
		}
		
        parent::__construct($course, $grade_item_params);                    
	}
	
	/*
        Creates a NumericGrade object and adds to the list (Called by ezMarker)
        
	Preconditions:
            $student: OrgMember object
            $grade_params: Python dictionary of parameters required to initialize a NumericGrade
        */
	function create_grade($student, $comment, $value){
  
        array_push($this->grades, NumericGrade($this, $student, $comment, $value));
        return;
	}
	
	/*
        Getter function
        
	Postconditions:
            Returns: $this->max_points - The max number of points this GradeItem can have for any one Grade
        */
	function get_max(){
        
        return $this->json['MaxPoints'];
	}
	
	/*
        Getter function
        
	Postconditions:
            returns: $this->can_exceed_max_points
        */
	function get_can_exceed(){
        return $this->json['CanExceedMaxPoints'];
	}
	
	function set_max($new_max){
       $old_max = $this->get_max();
       $this->json['MaxPoints'] = $new_max;
       try {
           put_grade_item($this);
       }
       catch (Exception $e) {
           error_log('Failed to update grade item ' . $this->get_id() . ' max from ' . $old_max . ' to ' . $new_max . '. ' . $e, 0);
           throw $e;
       }
       return;
	}
	
	/*
        Checks if a value is within below the max points of the grade object
        
	Preconditions:
            $value: the value to check against max_points
        
	Postconditions:
            Returns: Boolean - false if not value larger than maxa points 
        */
	function within_max($value){
        return ($value <= ($this->get_max()));
	}
}
?>

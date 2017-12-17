<?php
require_once "Grade.php";
require_once "API.php";
require_once 'OrgMember.php';

class GradeItem {
    protected $json;
    private $course;
    private $grades;

	public function __construct($course, $grade_item_params){
		/*
        Preconditions:
            $course (Course object) - the course the GradeItem is for
            $grade_item_params (json) - info about GradeItem  
            
        Postconditions:
            parent constructor to all GradeItem types. contains data common to all types
        */

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

	function get_name(){
		/*
        Getter function
        Postconditions:
            Returns: $this->name - name of the GradeItem
        */
		return $this->json['Name'];
	}
	function get_id(){
        /*
        Getter function
        Postconditions:
            Returns: $this->id - Id of the GradeItem
		*/
        return $this->json['Id'];
    }
    function get_grades(){
        /*
        Getter function
        Postconditions:
            Returns: List of Grade objects associated with this GradeItem
        */
        return $this->grades;
    }    
    function get_grade($student){
		/*
        Gets grade for a given student
        Preconditions:
            $student: OrgMember -> student whose grade we are looking for
        Postconditions:
            Returns: Grade object if there is a grade belonging to the student
                     Returns None if student grqade is not found
        */
        foreach($this->grades as $grade){
            if ($student->get_id() == $grade->get_student()->get_id()){
                return $grade;
			}
		}
        return null; 
	}
	
    function put_grades(){
        /*
        Calls $grade->put_grade() for each Grade object
        */
        foreach ($this->grades as $grade){
            $grade->put_grade();
		}
        return;
	}
		
    function put_grade_item(){
        /*
        Puts grade item to Brightspace
        */
        put_grade_item($this);
        return;
    }    
	
    function get_user(){
        /*
        Getter function
        Postconditions:
            Returns: User object - User associated with the GradeItem
        */
        return ($this->course->get_user());
	}
	
    function get_course(){
        /*
        Getter function
        Postconditions:
            Returns: $this->course - Course that the GradeItem belongs to
        */
        return $this->course;
	}
}
class NumericGradeItem extends GradeItem {
	public function __construct($course, $grade_item_params){
		/*
        Preconditions:
            $course (Course object) - the course the NumericGradeItem is for
            $grade_item_params (json) - info about GradeItem (Grade.GradeObject: GradeType must be numeric!) 
            
        Postconditions:
            creates object of type NumericGradeItem
        */
		
		if ($grade_item_params["GradeType"] != "Numeric") {
			$course_id = $course->get_id();
			$the_grade_item = $grade_item_params["Id"];
            throw new RuntimeException("GradeType for GradeItem " . $course_id . "of Course " . $the_grade_item . " is not numeric.");
		}
		
        parent::__construct($course, $grade_item_params);                    
	}
	
	function create_grade($student, $comment, $value){
        /*
        Creates a NumericGrade object and adds to the list (Called by ezMarker)
        Preconditions:
            $student: OrgMember object
            $grade_params: Python dictionary of parameters required to initialize a NumericGrade
        */
        array_push($this->grades, NumericGrade($this, $student, $comment, $value));
        return;
	}
	
	function get_max(){
        /*
        Getter function
        Postconditions:
            Returns: $this->max_points - The max number of points this GradeItem can have for any one Grade
        */
        return $this->json['MaxPoints'];
	}
	
	function get_can_exceed(){
        /*
        Getter function
        Postconditions:
            returns: $this->can_exceed_max_points
        */
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
	
	function within_max($value){
        /*
        Checks if a value is within below the max points of the grade object
        preconditions:
            $value: the value to check against max_points
        Postconditions:
            Returns: Boolean - false if not value larger than maxa points 
        */
        
        return ($value <= ($this->get_max()));
	}
}
?>
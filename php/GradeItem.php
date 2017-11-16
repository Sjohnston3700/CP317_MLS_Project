<?php
	include_once "Grade.php";
	include_once "API.php";

class GradeItem {
	
	
	public function __construct($course, $grade_item_params){
		/*
        Preconditions:
            course (Course object) - the course the GradeItem is for
            grade_item_params (json) - info about GradeItem  
            
        Postconditions:
            parent constructor to all GradeItem types. contains data common to all types
        */
		
		if ((gettype($this)) == GradeItem){
			throw new RuntimeException("GradeItem must be subclassed");
		}
		
		$this->name = $grade_item_params("Name");
        $this->id = $grade_item_params("Id");
        $this->course = $course;
        $this->grades = array();
	}
	
	function get_name(){
		/*
        Getter function
        Postconditions:
            Returns: self._name - name of the GradeItem
        */
		return $this->name;
	}
	
	function get_id(){
        /*
        Getter function
        Postconditions:
            Returns: self._id - Id of the GradeItem
		*/
        return $this->id;
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
            student: OrgMember -> student whose grade we are looking for
        Postconditions:
            Returns: Grade object if there is a grade belonging to the student
                     Returns None if student grqade is not found
        */
        foreach($this->grades as $grade){
            if ($student->get_id() == $grade->get_student()->get_id()){
                return $grade;
			}
		}
        return Null
       
	}
	
    function put_grades(){
        /*
        Calls grade.put_grade() for each Grade object
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
        API->put_grade_item($this);
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
            Returns: self._course - Course that the GradeItem belongs to
        */
        return $this->course;
	}
	
}
?>
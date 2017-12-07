<?php 

	require_once 'API.php';

	
class Grade {
	/*
	Constructor:
		grade_item(GradeItem Object)
		student(OrgMember)
		comment (String)
	*/
	function __construct($grade_item, $student, $comment) {
		$this->grade_item = $grade_item;
		$this->student = $student;
		$this->comment = $comment;
	}
	/*
	Return comments for this student with respect to this GradeItem
	*/
	function get_comment(){
		
		return $this->comment; 
	}
	/*
	Return the GradeItem Object
	*/
	function get_grade_item(){
		return $this->grade_item; 
		 
		
	}
	
	/*
	Return the student object (OrgMember)
	*/
	function get_student(){
		return $this->student;  
	}
	
	/*
	Call function to update grade
	*/
	function put_grade(){
		put_grade(); 

	}
}
class NumericGrade extends Grade{
	/*
	Constructor:
		grade_item(GradeItem Object)
        student(OrgMember)
        comment(feedbacks) string
        value(mark student scored) float
	*/
	function __construct($grade_item, $student, $comment, $value) {
		
		parent::__construct($grade_item, $student, $comment);
		
		$this->value = $value;	
		 
	}
	/*
	Returns value of the NumericGrade Item
	*/
	function get_value() {
		return $this->value;  
	}
	
}


?>
<?php 

	require_once 'API.php';
	$FEEDBACK_PATTERN = '\-{3,}?.*?(\d{5,7}).*?^([\w|\s]*?)$(.+?(?:Total:\s+(\d+)\s+\/\s+(\d+).*?)?)\-{3,}?'


class Grade{
	
	function __construct($grade_item, $student, $comment) {
		
		/*
		Constructor:
            grade_item(GradeItem Object)
            student(OrgMember)
            comment (String)
		*/
		
		$this->_grade_item = grade_item;
		$this->_student = student;
		$this->_comment = comment;
	
	}
	
	function get_comment(){
		
		/*
		Return comments for this student with respect to this GradeItem
		*/
		
		return $this->comment; 
	
		
	}
	
	function get_grade_item(){
		
		/*
		Return the GradeItem Object
		*/
		
		return $this->grade_item; 
		 
		
	}
	
	
	function get_student(){
		/*
		Return the student object (OrgMember)
		*/
		return $this->student;  
		 
		
		
	}
	
	function get_user(){
		
		/*
		Return the user
		*/
		
		return $this->grade_item.get_user()  
		
		
	}
	
	function put_grade(){
		
		/*
		Call function to update grade
		*/
		API.put_grade(); 

	}
	
class NumericGrade{
	
	function __construct($grade_item, $student, $comment, $value) {
		
		/*
		Constructor:
            grade_item(GradeItem Object)
            student(OrgMember)
            comment(feedbacks) string
            value(mark student scored) float
		*/
		
		parent::__construct($grade_item, $student, $comment);
		
		$this->_value = value;	
		 
	}
		
	function get_value() {
		
		/*
		Returns value of the NumericGrade Item
		*/
		
		return $this->value;  
		
		
	}
	
}
}

?>
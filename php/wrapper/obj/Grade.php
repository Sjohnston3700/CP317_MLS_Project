<?php 

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
		return $this->_comment;
	}
	
	function get_grade_item(){
		/*
		Return the GradeItem Object
		*/
		return $this->_grade_item;
	}
	
	
	function get_student(){
		/*
		Return the student object (OrgMember)
		*/
		return $this->_student;
	}
	
	function get_user(){
		/*
		Return the user
		*/
		return self._grade_item.get_user()
		
	}
	
	function put_grade(){
		/*
		Call function to update grade
		*/
		API.put_grade();
	}
}

?>
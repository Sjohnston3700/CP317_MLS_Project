<?php

session_start();
require_once('../../includes/functions/grade_functions.php');

// Need error checkinf for grades, course, grade_item etc
$grades = $_REQUEST['grades'];
$course = $_REQUEST['course'];
$grade_item = $_REQUEST['grade_item'];

$errors = error_checking($grades, $course, $grade_item);

if (sizeof($errors) > 0)
{
	echo json_encode($errors);	
}
else 
{
	echo json_encode(array());
}

?>


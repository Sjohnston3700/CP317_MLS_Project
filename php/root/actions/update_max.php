<?php

session_start();
require_once('../../includes/functions/grade_functions.php');

$max = $_REQUEST['max'];
$course = $_REQUEST['course'];
$grade_item = $_REQUEST['grade_item'];
$errors = modify_grade_max($course, $grade_item, $max);

if (sizeof($errors) > 0)
{
	echo json_encode($errors);	
}
else 
{
	echo json_encode(array());
}

?>
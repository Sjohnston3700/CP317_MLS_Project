<?php

session_start();
require_once('../../includes/functions/grade_functions.php');

if (!isset($_REQUEST['grades']) || !isset($_REQUEST['course']) || !isset($_SESSION['userId']) || !isset($_SESSION['userKey']))
{
	die();
}

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


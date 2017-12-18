<?php
/**
 * @file
 * Controller for sending grades to be checked
 */

session_start();
require_once '../../includes/functions/grade_functions.php';

// If no course or user tokens set, the user is doing something suspicious, so don't continue
if (!isset($_REQUEST['course']) || !isset($_SESSION['user'])) {
    die();
}

// If user submits no grades, send error to frontend and don't continue
if (!isset($_REQUEST['grades'])) {
    $errors = array();
    $msg = array( 'error' => "You didn't submit any grades");
    $errors[] = $msg;
    echo json_encode($errors);    
    die();
}

$grades = $_REQUEST['grades'];
$course = $_REQUEST['course'];
$grade_item = $_REQUEST['grade_item'];

$errors = check_grades($grades, $course, $grade_item);

if (sizeof($errors) > 0) {
    echo json_encode($errors);    
} else 
{
    echo json_encode(array());
}

?>

<?php
/**
 * @file
 * Controller for updating grade item max
 */

session_start();
require_once '../../includes/functions/grade_item_functions.php';

if (!isset($_REQUEST['max']) || !isset($_REQUEST['course']) || !isset($_REQUEST['grade_item']) || !isset($_SESSION['user'])) {
    $error = array( 'msg' => 'Bad request, you have missing parameters' );
    echo json_encode($error);
    die();
}

$max = $_REQUEST['max'];
$course = $_REQUEST['course'];
$grade_item = $_REQUEST['grade_item'];
$response= modify_grade_max($course, $grade_item, $max);

// Array of errors or value of new max
echo json_encode($response);    

?>

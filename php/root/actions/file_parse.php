<?php

session_start();
require_once('../../includes/functions/grade_functions.php');

if (!isset($_SESSION['userId']) || !isset($_SESSION['userKey']))
{
	die();
}

if (!isset($_FILES['file']) || $_FILES['file']['tmp_name'] == '')
{
	$msg = array( 'msg' => 'No file was submitted' );
	$error = array();
	$error[] = $msg;
	echo json_encode($error);
	die();
}

//test if proper file type
//no point in checking each line for validity if wrong type
$allowed =  array('csv','txt');
$ext = pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION);
if(!in_array($ext, $allowed) ) {
    $msg = array( 'msg' => 'Incorrect file type. Must be .csv or .txt' );
	$error = array();
	$error[] = $msg;
	echo json_encode($error);
	die();
}

// Open CSV
$file = fopen($_FILES['file']['tmp_name'], 'r');

if (!$file)
{
	$msg = array( 'msg' => 'No file was submitted' );
	$error = array();
	$error[] = $msg;
	echo json_encode($error);
	die();
}

$grades = parse_file($file);
fclose($file);

// Return JSON object to frontend
echo json_encode($grades);

?>
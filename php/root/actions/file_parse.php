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
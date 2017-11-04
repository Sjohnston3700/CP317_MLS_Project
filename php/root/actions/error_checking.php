<?php

require_once('../../includes/functions/upload_functions.php');
$grades = $_REQUEST['grades'];
$errors = error_checking($grades, 1);
if (sizeof($errors) > 0)
{
	echo json_encode($errors);	
}
else 
{
	echo 200;
}

?>
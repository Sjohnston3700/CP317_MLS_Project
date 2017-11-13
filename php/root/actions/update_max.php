<?php

require_once('../../includes/functions/grade_functions.php');
$max = $_REQUEST['max'];
$errors = modify_grade_max(1, $max);
if (sizeof($errors) > 0)
{
	echo json_encode($errors);	
}
else 
{
	echo json_encode(array());
}

?>
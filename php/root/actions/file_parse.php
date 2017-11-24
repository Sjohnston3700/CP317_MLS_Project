<?php
require_once('../../includes/functions/grade_functions.php');

// Open CSV
$file = fopen($_FILES['file']['tmp_name'], 'r');
$grades = parse_file($file);
fclose($file);

// Return JSON object to frontend
echo json_encode($grades);

?>
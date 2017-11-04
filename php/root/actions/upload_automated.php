<?php

$grades = array();

// Open CSV
$file = fopen($_FILES['file']['tmp_name'], 'r');

// Traverse through CSV and add each pseudo Grade object to JSON object
while (!feof($file))
{
 	$row = fgetcsv($file);
	$grade = array(
		'id' => $row[0],
		'value' => $row[1],
		'name' => $row[2],
		'comment' => $row[3]
	);
		
	$grades[] = $grade;
}

// Close file
fclose($file);
// Return JSON object to frontend
echo json_encode($grades);

?>
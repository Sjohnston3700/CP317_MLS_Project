<?php 
	
/**
 * Parses Grade file (csv). Goes through file object and creates 
 * array of JSON grade objects.
 * @param {File} file - opened file object
 * @return {Array} Array of grade objects.
 */
function parse_file($file)
{
	$grades = array();
	$errors = array();
	$i = 1;
	$num_errors = 0;
	// Traverse through CSV and add each pseudo Grade object to JSON object
	while (!feof($file))
	{	
		$row = fgetcsv($file);
		if (sizeof($row) < 4)
		{
			$error = array(
				'line' => $i,
				'msg' => 'Format must be student_name, brightspace_id, grade, comment'
			);
				
			$num_errors++;
			$errors[] = $error;
		}
		else 
		{
			$grade = array(
				'id' => $row[0],
				'value' => $row[1],
				'name' => $row[2],
				'comment' => $row[3]
			);

			$grades[] = $grade;
		}
		$i++;
	}

	if ($i - 1 == $num_errors)
	{	
		$msg = array();
		$msg[] = array(
			'msg' => 'Entire file is formatted incorrectly. Please ensure each student entry is formatted as student_name, brightspace_id, grade, comment'
		);
		return $msg;
	}
	else if ($num_errors > 0)
	{
		return $errors;
	}

	return $grades;
}

/**
 * Error checking for array of grades object. Returns array of errors.
 * @param {Array} grades - array of grades objects
 * @param {Integer} grade_item_id
 * @return {Array} Array of errors and error messages to be sent to frontend
 */
function error_checking($grades, $grade_item_id)
{	
	// Filler until grades class is done
	$grade_item = array(
		'max_points' => 30
	);
	
	// Error object to return it $error is true
	$errors = array();

	foreach ($grades as $g)
	{
		if ($g['value'] == '')
		{
			$errors[] = array ( 
				'id' => $g['id'],
				'value' => $g['value'],
				'name' => $g['name'],
				'comment' => $g['comment'],
				'msg' => 'Missing grade',
				'type' => '1' 
			);
		}
		else if (!is_numeric($g['value']))
		{
			$errors[] = array ( 
				'id' => $g['id'],
				'value' => $g['value'],
				'name' => $g['name'],
				'comment' => $g['comment'],
				'msg' => 'Grade must be a number',
				'type' => '1' 
			);
		}
		else if ($g['value'] < 0)
		{
			$errors[] = array ( 
				'id' => $g['id'],
				'value' => $g['value'],
				'name' => $g['name'],
				'comment' => $g['comment'],
				'msg' => 'Grade cannot be negative',
				'type' => '1'
			);
		}
		else if ($g['value'] > $grade_item['max_points'])
		{
			$errors[] = array ( 
				'id' => $g['id'],
				'value' => $g['value'],
				'name' => $g['name'],
				'comment' => $g['comment'],
				'msg' => 'Grade is more than the grade maximum',
				'type' => '0'
			);
		}
	}
	return $errors;
}

?>
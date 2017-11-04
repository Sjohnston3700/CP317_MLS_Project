<?php 
	

function parse_file($file)
{
	$grades = array();
	
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

	return $grades;
}

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
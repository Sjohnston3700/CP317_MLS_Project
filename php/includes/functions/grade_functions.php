<?php 
	
require_once('../../wrapper/obj/API.php');
require_once('../../wrapper/obj/OrgMember.php');
require_once('../../wrapper/obj/Grade.php');
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
function error_checking($grades, $course_id, $grade_item_id)
{	
	$user = new User(array());
	$course = get_course($user, $course_id);
	$course = new Course($user, $course);
	$grade_item = $course->get_grade_item($grade_item_id);
	
	//****** TO DO ERROR HANDLING check if course and grade_item actually exist and if user has permission ******
	// Error object to return
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
		else if ($g['value'] > $grade_item->get_max() && $grade_item->get_can_exceed())
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
		else if ($g['value'] > $grade_item->get_max() && !$grade_item->get_can_exceed())
		{
			$errors[] = array ( 
				'id' => $g['id'],
				'value' => $g['value'],
				'name' => $g['name'],
				'comment' => $g['comment'],
				'msg' => 'Grade is more than the grade maximum',
				'type' => '1'
			);
		}
	}

	if (sizeof($errors) == 0)
	{
		return upload_grades($grades, $course, $grade_item);
	}
	return $errors;
}

function upload_grades($grades, $course, $grade_item)
{
	$errors = array();
	
	foreach ($grades as $g)
	{	
		$id = $g['id'];
		$student = $course->get_member($id);
		$grade = new NumericGrade($grade_item, $student, $g['comment'], $g['value']);
		put_grade($grade);
	}
	
	return $errors;
}
/**
 * Error checking for max. If success, updates max grade value
 * @param {Integer} grade_item_id
 * @param {Integer} max
 * @return {Array} Array of errors and error messages to be sent to frontend
 */
function modify_grade_max($course_id, $grade_item_id, $max)
{
	$user = new User(array());
	$course = get_course($user, $course_id);
	$course = new Course($user, $course);
	$grade_item = $course->get_grade_item($grade_item_id);

	// Error object to return
	$errors = array();
	if ($max === '')
	{
		$errors[] = array ( 
			'msg' => 'Missing grade maximum',
		);
	}
	else if (!is_numeric($max))
	{
		$errors[] = array ( 
			'msg' => 'Grade maximum must be a number',
		);
	}
	else if (floatval($max) < 0)
	{
		$errors[] = array ( 
			'msg' => 'Grade maximum must be a positive number',
		);
	}

	if (sizeof($errors) == 0)
	{
		$grade_item->set_max((float)$max);
		return put_grade_item($grade_item, get_grade_item($course_id, $grade_item_id));
	}
	return $errors;
}

?>
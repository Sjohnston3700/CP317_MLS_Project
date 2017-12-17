<?php 
	
require_once('../../wrapper/obj/API.php');
require_once('../../wrapper/obj/User.php');
require_once('../../wrapper/obj/Grade.php');
require_once('../../wrapper/obj/GradeItem.php');
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
			//no error if last line is empty (common occurence if manually editing in Excel, for example)
			if ($row == NULL) {
				if (feof($file)) {
					$i++;
					break;
				}
				//else
				$error = array(
					'line' => $i,
					'msg' => ''
				);
			}
			else {
				$error = array(
					'line' => $i,
					'msg' => $row
				);
			}
				
			$num_errors++;
			$errors[] = $error;
		}
		//require that there must be some value for id, grade, name
		else if (trim($row[0]) == '' || trim($row[1]) == '' || trim($row[2]) == '') {
			$error = array(
				'line' => $i,
				'msg' => $row
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
			'msg' => 'Entire file is formatted incorrectly. Please ensure each student entry is formatted as brightspace_id, grade, student_name, comment'
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
 * @param {Array} array - parent array to search
 * @param {String} key - key to use in subarray
 * @param {String} val - val to look for  in subarray
 * @return {Array} subarray containing val for key
 */
function findSubarray($array, $key, $val) {
	for ($i = 0; $i < sizeof($array); $i++) {
		if ($array[$i][$key] == $val) {
			return $i;
		}
	}

	return -1;
}

/**
 * Error checking for array of grades object. Returns array of errors.
 * Expects that array is ordered like the file (if applicable). For putting line# in error msg
 * @param {Array} grades - array of grades objects
 * @param {Integer} grade_item_id
 * @return {Array} Array of errors and error messages to be sent to frontend
 */
function error_checking($grades, $course_id, $grade_item_id)
{	
	$user = unserialize($_SESSION['user']);
	$course = $user->get_course($course_id);

	$grade_item = $course->get_grade_item($grade_item_id);
	
	// Error object to return
	$errors = array(); 
	//object to track errors that result in error-modal not displaying
	//errors so bad they completely 'fail' upload. If any fail errors, only those returned
	$fail_errors = array(); 
	//counts occurences of each id. Used to check for duplicate ids (possible if uploaded from file)
	$id_count = array_count_values(array_column($grades, 'id'));
	//for tracking the line number (used if error is one that only file upload would have)
	$i = 0;

	foreach ($grades as $g)
	{	
		$i++;
		//if duplicate id
		if($id_count[$g['id']] > 1) {
			//if haven't already recorded duplicate error
			if(!in_array($g['id'], array_column($fail_errors, 'id'))) {
				$fail_errors[] = array ( 
					'line' => $i,
					'id' => $g['id'],
					'msg' => 'MLS ID '. $g['id'] . ' is duplicated',
					'type' => '2' 
				);
			}
			//if have already recorded duplicate error, add new line# to existing entry
			else {
				$index = findSubarray($fail_errors, 'id', $g['id']);
				if ($index >= 0) {
					$fail_errors[$index]['line'] = $fail_errors[$index]['line'] . ', ' . $i;
				}
				continue;
			}
		}
		if ($course->get_member($g['id']) == null)
		{
			$fail_errors[] = array ( 
				'line' => $i,
				'id' => $g['id'],
				'msg' => 'Student '. $g['name'] . ' not found for course',
				'type' => '2' 
			);
		}
		else if ($g['value'] == '')
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
		//for if you want to send a warning msg if grade > max and that is allowed by gradeitem
		//client, as of Dec. 6, 2017, does not want this feature
		//but leaving in file in case someone desires this later
		//implementing this again would require minor changes to upload.sendToErrorChecking
		/* else if ($g['value'] > $grade_item->get_max() && $grade_item->get_can_exceed())
		{	
			
			if (!isset($g['is_warning']) || isset($g['is_warning']) && $g['is_warning'] == false)
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
			else 
			{
				$ids[]= $g['id'];
			}
		} */
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

	//only return 1 error object. fail_errors is priority (upload not worth sending to modal)
	if (sizeof($fail_errors) != 0) {
	 	$errors = $fail_errors;
	}

	return $errors;
}

function upload_grades($grades, $course_id, $grade_item_id)
{

	$user = unserialize($_SESSION['user']);
	$course = $user->get_course($course_id);
	$grade_item = $course->get_grade_item($grade_item_id);
	
	$errors = array();
	$sucessful_ids = array();
	
	foreach ($grades as $g)
	{	
		$id = $g['id'];
		$student = $course->get_member($id);
		$grade = new NumericGrade($grade_item, $student, $g['comment'], $g['value']);
		
		// If no errors, add to successful_ids array
		if (sizeof(put_grade($grade) == 0))
		{
			$sucessful_ids[] = $id;
		}
	}
	if (sizeof($errors) == 0)
	{
		return $sucessful_ids;	
	}
	// If $errors is empty or the first element is numeric, go to report page. 
	// If the value is numeric, this means $errors is a list of successful $ids
	if (sizeof($errors) == 0 || (isset($errors[0]) && is_numeric($errors[0]))) 
	{	
		$successful_ids = $errors;
		$_SESSION['report'] = array(
			'total' => sizeof($grades),
			'successful' => sizeof($successful_ids),
			'successful_ids' => $successful_ids
		);	
	} 
	else
	{
		$_SESSION['report'] = array(
			'errors' => $errors
		);
	}

	//store user object that possibly contains modified objects
	$_SESSION['user'] = serialize($user);
	
	return array();
}

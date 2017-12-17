<?php 

require_once('../../wrapper/obj/API.php');
require_once('../../wrapper/obj/User.php');
require_once('../../wrapper/obj/GradeItem.php');
/**
 * Error checking for max. If success, updates max grade value
 * @param {Integer} grade_item_id
 * @param {Integer} max
 * @return {Array} Array of errors and error messages to be sent to frontend
 */
function modify_grade_max($course_id, $grade_item_id, $max)
{
	$user = unserialize($_SESSION['user']);
	$course = $user->get_course($course_id);
	$grade_item = $course->get_grade_item($grade_item_id);
	

	// Error object to return
	$errors = array();
	if ($max === '')
	{
		$errors[] = array ( 
			'msg' => 'Missing grade maximum'
		);
	}
	else if (!is_numeric($max))
	{
		$errors[] = array ( 
			'msg' => 'Grade maximum must be a number'
		);
	}
	else if (floatval($max) <= $grade_item->get_max())
	{
		$errors[] = array ( 
			'msg' => 'New grade maximum must be larger than current maximum'
		);
	}

	if (sizeof($errors) == 0)
	{
		$grade_item->set_max((float)$max);
		//store user that contains modified gradeitem
		$_SESSION['user'] = serialize($user);
		return put_grade_item($grade_item);
	}
	return $errors;
}

?>

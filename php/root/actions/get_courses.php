<?php

require_once('../../wrapper/obj/User.php');

session_start();

function comp($item1, $item2) {
    return strcmp($item2['name'], $item1['name']);
}

// If no course or user tokens set, the user is doing something suspicious, so don't continue
if (!isset($_SESSION['user']))
{
	die();
}

$user = unserialize($_SESSION['user']);
$courses = array();

foreach($user->get_courses() as $course) {
    $data = array(
        'name' => $course->get_name(),
        'id' => $course->get_id(),
        'grade_items' => array()
    );

    foreach($course->get_grade_items() as $grade_item) {
        array_push($data['grade_items'], array(
            'name' => $grade_item->get_name(),
            'id' => $grade_item->get_id()
        ));
    }
    array_push($courses, $data);
}

usort($courses, 'comp');

echo json_encode($courses);

?>


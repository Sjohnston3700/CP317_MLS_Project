<?php
/**
 * @file
 * Controller for getting courses for courses page
 */

require_once '../../wrapper/obj/User.php';

session_start();

//comparator for courses
//results in dsc order
function comp($item1, $item2) 
{
    return strcmp($item2['name'], $item1['name']);
}

// If no course or user tokens set, the user is doing something suspicious, so don't continue
if (!isset($_SESSION['user'])) {
    die();
}

$user = unserialize($_SESSION['user']);
$courses = array();

foreach ($user->get_courses() as $course) {
    $data = array(
        'name' => $course->get_name(),
        'id' => $course->get_id(),
        'grade_items' => array()
    );

    foreach ($course->get_grade_items() as $grade_item) {
        array_push(
            $data['grade_items'], array(
            'name' => $grade_item->get_name(),
            'id' => $grade_item->get_id()
            )
        );
    }
    array_push($courses, $data);
}

//store user object that now has courses
$_SESSION['user'] = serialize($user);

//sort in dsc order of name, so that in asc order as courses inserted
usort($courses, 'comp');

echo json_encode($courses);

?>
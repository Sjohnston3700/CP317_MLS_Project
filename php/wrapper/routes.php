<?php

require_once '../root/config.php';

$API_ROUTE = '/d2l/api/versions/';
$GET_GRADES_ROUTE     = '/d2l/api/le/(version)/(orgUnitId)/grades/';
$SET_GRADE_ROUTE      = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)';
$GET_COURSE_MEMBERS   = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/';
$GET_USER_ENROLLMENTS = '/d2l/api/lp/(version)/enrollments/myenrollments/';
$GET_USER_ENROLLMENT  = '/d2l/api/le/(version)/(orgUnitId)/grades/';
$GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami';

?>
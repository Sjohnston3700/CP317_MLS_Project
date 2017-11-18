<?php

require_once '../root/config.php';

$HOST = $config['lms_host'];
$VER = $config['LP_Version'];

$API_ROUTE = $HOST. '/d2l/api/versions/';
$GET_GRADES_ROUTE     = $HOST . '/d2l/api/le/' . $VER . '/(orgUnitId)/grades/';
$SET_GRADE_ROUTE      = $HOST . '/d2l/api/le/' . $VER . '/(orgUnitId)/grades/(gradeObjectId)/values/(userId)';
$GET_COURSE_MEMBERS   = $HOST . '/d2l/api/lp/' . $VER . '/enrollments/orgUnits/(orgUnitId)/users/';
$GET_USER_ENROLLMENTS = $HOST . '/d2l/api/lp/' . $VER . '/enrollments/myenrollments/';
$GET_USER_ENROLLMENT  = $HOST . '/d2l/api/le/' . $VER . '/(orgUnitId)/grades/';
$GET_WHO_AM_I         = $HOST . '/d2l/api/lp/' . $VER . '/users/whoami';

?>
<?php
$config = array(
	'libpath'    => '../D2Llib',
	'host'       => 'localhost',
	'port'       => '8080', 
	'lms_host'	 => 'wlutest.desire2learn.com',
	'lms_port'   => '443',
	'scheme'     => 'https',
	'encrypt_requests' => true,
	'route'      => '/token',
	'appId'     => 'FNWvubihLM8CICkHONZ_aw',
	'appKey'    => 'OrL8HleCxiyuG8JBd7DEPg', 
	'LP_Version' => '1.0'
);


$routes = array(
	'BASE_URL' 				=> $config['scheme'] . '://' . $config['lms_host'],
	'API_ROUTE' 		    => '/d2l/api/versions/',
	'GET_GRADES_ROUTE'     => '/d2l/api/le/(version)/(orgUnitId)/grades/',
	'SET_GRADE_ROUTE'      => '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)',
	'GET_COURSE_MEMBERS'   => '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/',
	'GET_USER_ENROLLMENTS' => '/d2l/api/lp/(version)/enrollments/myenrollments/',
	'GET_USER_ENROLLMENT'  => '/d2l/api/le/(version)/(orgUnitId)/grades/',
	'GET_WHO_AM_I'         => '/d2l/api/lp/(version)/users/whoami',
);

//Localhost
//Application ID: FNWvubihLM8CICkHONZ_aw
//Application Key: OrL8HleCxiyuG8JBd7DEPg
//
//Somethingdumb
//Application ID: 7EgSmt25Zi_WDQg9QbnjZA
//Application Key: MeXB--LewCR7f7ZQlPgKYw

<?php
require_once _DIR_.'/../../root/config.php';
require_once _DIR_.'/../../D2Llib/D2LAppContextFactory.php';

$routes = array(
	'BASE_URL' 				=> $config['protocol'] . '://' . $config['lms_host'],
	'GET_API_VERSIONS' 	   => '/d2l/api/versions/',
	'GET_GRADES'     	   => '/d2l/api/le/(version)/(orgUnitId)/grades/',
	'SET_GRADE'            => '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)',
	'GET_COURSE_MEMBERS'   => '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/',
	'GET_USER_ENROLLMENTS' => '/d2l/api/lp/(version)/enrollments/users/(userId)/orgUnits/',
	'GET_USER_ENROLLMENT'  => '/d2l/api/le/(version)/(orgUnitId)/grades/',
	'GET_WHO_AM_I'         => '/d2l/api/lp/(version)/users/whoami',
	'GET_GRADE_VALUES'	   => '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/',
	'SET_GRADE_MAX'		   => '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)',
	'GET_GRADE'			   => '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)'
);

//{
//"GradeObjectType": 1, 
//"PointsNumerator": 12
//}
   	);

	$response = get($routes['GET_USER_ENROLLMENTS'], $route_params);
	
	foreach ($response['Items'] as $c) {
		if ($c['OrgUnit']['Id'] == $course_id) {
			return $c;
		}
	}
	return -1;
}

function get_grade_item($course_id, $grade_item_id) {
	global $config;
	global $routes;

	$route_params = array(
		 'version' => $config['LP_Version'],
		 'orgUnitId' => $course_id, 
		 'gradeObjectId' => $grade_item_id
	);

	$response = get($routes['GET_GRADE'], $route_params);
	
	return $response;
}
function get_grade_items($course){
	global $config;
	global $routes;

	$route_params = array(
		 'version' => $config['LP_Version'],
		 'orgUnitId' => $course->get_id()
		);

	$response = get($routes['GET_GRADES'], $route_params);
	return $response;
}

function get_grade_values($course_id, $grade_item_id) {
	global $config;
	global $routes;
	
	$route_params = array(
		'version' => '1.8',
		'orgUnitId' => $course_id,
		'gradeObjectId' => $grade_item_id
	);
	$response = get($routes['GET_GRADE_VALUES'], $route_params);
	return $response['Objects'];
}

/*
Retrieves the collection of users enrolled in the identified org unit.

Preconditions:
	user (Course object) : A Course object to retrieve grades from.

Postconditions:
	returns:
	user_enrollments (dict) : A dict of user_enrollment data corresponding to the given User object.
*/
function get_user_enrollments($user){

	global $config;
	global $routes;

	$route_params = array(
		'version' => $config['LP_Version'],
		'userId' => $user->get_id(),
	);
	$response = get($routes['GET_USER_ENROLLMENTS'], $route_params);
	return $response['Items'];
}

function get_members($course) {
	global $config;
	global $routes;
	
	$route_params = array(
		'version' => $config['LP_Version'],
		'orgUnitId' => $course->get_id(),
	);
	
	$response = get($routes['GET_COURSE_MEMBERS'], $route_params);
	if (array_key_exists('Items', $response)) {
		return $response['Items'];
	}
	else {
		return array();
	}
}

function get_who_am_i() {
	global $config;
	global $routes;
	
	$route_params = array('version' => $config['LP_Version']);
	$response = get($routes['GET_WHO_AM_I'], $route_params);
	
	return $response;
}

function put($route, $route_params, $json_to_send) {
	/*
	Uses a PUT request to set JSON

	Preconditions :
		grade_item (GradeItem object) : The grade_item to change grade data for
		params (json) : JSON grade data to send
	Postconditions:
		Brightspace data will be updated with params as JSON
	*/

	global $routes;

	$route = update_route($routes['BASE_URL'] . $route, $route_params);
//	print_r(json_encode($json_to_send));
//	die();
	$response = valence_request($route, 'PUT', json_encode($json_to_send));

	return $response;
}

function put_grade($grade){
	/*
	Posts a Grade object to Brightspace using a PUT request

	Preconditions:
		grade : the grade to post
	Postconditions:
		grade JSON is PUT to Brightspace
	*/
	global $config;
	global $routes;
	
	$route_params = array(
		'version'=> '1.12',
		'orgUnitId' => $grade->get_grade_item()->get_course()->get_id(),
		'gradeObjectId' => $grade->get_grade_item()->get_id(),
		'userId' => $grade->get_student()->get_id(),
	);

	$params = array(
		'GradeObjectType' => 1,
		'PointsNumerator' => $grade->get_value(),
		'Comments' => array('Content' => $grade->get_comment(), 'Type' => 'Text'), 
		'PrivateComments' => array('Content' => '', 'Type' => 'Text'));

	# Make PUT request
	$response = put($routes['SET_GRADE'], $route_params, $params);

	return json_encode($response);

}

function put_grade_item($grade_item, $original){
	/*
	Posts a GradeItem object to Brightspace using a PUT request

	Preconditions:
		grade_item : the grade_item to post
	Postconditions:
		grade_item JSON is PUT to Brightspace
	*/
	
	global $config;
	global $routes;
	
	$route_params = array(
		'version' => $config['LP_Version'],
		'orgUnitId' => $grade_item->get_course()->get_id(),
		'gradeObjectId' => $grade_item->get_id()
	);
	
	if (empty($original['IsBonus']))
		$original['IsBonus'] = false;
	
	$params = array(
		'MaxPoints' => $grade_item->get_max(), 
		'CanExceedMaxPoints' => $grade_item->get_can_exceed(), 
		'GradeType' => 'Numeric',
		'IsBonus' => $original['IsBonus'],
		'ExcludeFromFinalGradeCalculation' => $original['ExcludeFromFinalGradeCalculation'],
		'GradeSchemeId' => $original['GradeSchemeId'],
		'Name' => $original['Name'],
		'ShortName' => $original['ShortName'],
		'CategoryId' => $original['CategoryId'],
		'Description' => array('Content' => $original['Description']['Html'], 'Type' => 'Html')
	);
	
	$response = put($routes['SET_GRADE_MAX'], $route_params, $params);
	if (isset($response['MaxPoints'])) {
		return $response['MaxPoints'];
	}
	return json_encode($response);
}

/*
Function to update api route by replace (...) with the appropriate value

Preconditions: 
	route: the route from the valence docs (eg. '/d2l/api/le/(version)/(orgUnitId)/grades/')
	params: dictionary of replacement values (eg {'version':1.22,'orgUnitId':23456})

Postconditions:
	Returns new route - Does not check for missed values
*/
function update_route($route, $params) {
	if ($params != null){
		foreach ($params as $key => $value){
			$route = str_replace('(' . $key . ')', $value, $route); //Control structure issue, no spaces before or after parenthesis
		} 
	}
	return $route;
}


function valence_request($route, $verb, $json_to_send) {
	global $routes;
	global $config;

	$userId = $_SESSION['userId'];
	$userKey = $_SESSION['userKey'];

	// Create authContext
	$authContextFactory = new D2LAppContextFactory();
	$authContext = $authContextFactory->createSecurityContext($config['appId'], $config['appKey']);

	// Create userContext
	$hostSpec = new D2LHostSpec($config['lms_host'], $config['lms_port'], $config['protocol']);
	$userContext = $authContext->createUserContextFromHostSpec($hostSpec, $userId, $userKey);
	
	// Create url for API call
	$uri = $userContext->createAuthenticatedUri($route, $verb);
	// Setup cURL
	$ch = curl_init();
	$options = array(
		CURLOPT_RETURNTRANSFER => true,
		CURLOPT_CUSTOMREQUEST  => $verb,
		CURLOPT_URL            => $uri,
		CURLOPT_SSL_VERIFYPEER => false,
		CURLINFO_HEADER_OUT => true
	);
	if (sizeof($json_to_send) > 0) {
		$options[CURLOPT_POSTFIELDS] = $json_to_send;
		$options[CURLOPT_HTTPHEADER] = 
			array(                                                                          
			'Content-Type: application/json',                                                                                
			'Content-Length: ' . strlen($json_to_send));
	}

	curl_setopt_array($ch, $options);

	$response = curl_exec($ch);
	$httpCode  = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	$contentType = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
	$responseCode = $userContext->handleResult($response, $httpCode, $contentType);
	
	return json_decode($response, true);

	$errors = curl_error($ch);
	throw new Exception('Valence API call failed: $httpCode: $response');
}
?>
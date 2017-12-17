<?php
require_once __DIR__.'/../../root/config.php';
require_once __DIR__.'/../../D2Llib/D2LAppContextFactory.php';
require_once('User.php');
require_once('Grade.php');
require_once('GradeItem.php');
require_once('Course.php');
require_once('OrgMember.php');

$routes = array(
	'BASE_URL' 			   => $config['protocol'] . '://' . $config['lms_host'],
	'GET_API_VERSIONS' 	   => '/d2l/api/versions/',
	'GET_GRADE_ITEMS'      => '/d2l/api/le/(version)/(orgUnitId)/grades/',
	'SET_GRADE'            => '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)',
	'GET_COURSE_ENROLLMENTS'   => '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/',
	'GET_USER_ENROLLMENTS' => '/d2l/api/lp/(version)/enrollments/users/(userId)/orgUnits/',
	'GET_MY_ENROLLMENTS'   => '/d2l/api/lp/(version)/enrollments/myenrollments/',
	'GET_WHO_AM_I'         => '/d2l/api/lp/(version)/users/whoami',
	'GET_GRADE_VALUES'	   => '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/',
	'SET_GRADE_ITEM'		   => '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)',
	'GET_GRADE_ITEM'	   => '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)'
);
/*
Uses a GET request to get JSON

Preconditions:
	user - A User object corresponding to the current user
	route - The route to make a GET request to
	route_params - A dictionary of parameters corresponding to route
	additional_params - A dictionary of extra parameters. Added to the end of the url as ?key=value
Postconditions
	On success:
		Returns:
		Python dict of request result
	On failure:
		raises RuntimeError
*/
function get($route, $route_params, $additional_params = array()){
	
		global $routes;
		
		$updated_route = update_route($routes['BASE_URL'] . $route, $route_params, $additional_params);
		$response = valence_request($updated_route, 'GET', array());

		if (array_key_exists('PagingInfo', $response) && $response['PagingInfo']['HasMoreItems'] == 'true'){
			$bookmark = $response['PagingInfo']['Bookmark'];
			$next_results = get($route, $route_params, $additional_params = array('bookmark='.$bookmark));

			//have to loop through since php adds '[' and ']' to append Items
			//if just use array_push($response['Items'], $next_results['Items'])
			foreach($next_results['Items'] as $item) {
				array_push($response['Items'], $item);
			}		
		}
		else if (array_key_exists('Next', $response) && !is_null($response['Next'])) {
			$next_results = get($response['Next'], array());

			//have to loop through since php adds '[' and ']' to append Items
			//if just use array_push($response['Items'], $next_results['Items'])
			foreach($next_results['Objects'] as $item) {
				array_push($response['Objects'], $item);
			}	
		}

		return $response;
	}
	
/*
Uses a PUT request to set JSON

Preconditions :
	grade_item (GradeItem object) : The grade_item to change grade data for
	params (json) : JSON grade data to send
Postconditions:
	Brightspace data will be updated with params as JSON
*/
function put($route, $route_params, $json_to_send) {
	global $routes;

	$route = update_route($routes['BASE_URL'] . $route, $route_params);
	$response = valence_request($route, 'PUT', json_encode($json_to_send));

	return $response;
}

/*
Function to update api route by replace (...) with the appropriate value

Preconditions: 
	route: the route from the valence docs (eg. '/d2l/api/le/(version)/(orgUnitId)/grades/')
	params: dictionary of replacement values (eg {'version':1.22,'orgUnitId':23456})

Postconditions:
	Returns new route - Does not check for missed values
*/
function update_route($route, $params, $additional_params = array()) {
	if ($params != NULL){
		foreach ($params as $key => $value){
			$route = str_replace('(' . $key . ')', $value, $route); //Control structure issue, no spaces before or after parenthesis
		} 
	}
	if (sizeof($additional_params) > 0) {
		$route .= '?';
		foreach($additional_params as $value) {
			$route .= $value;
		}
	}
	return $route;
}

/*
Function to get grade items from Brightspace of a certain course

Preconditions:
	course : The specific course to pull from
Postconditions:
	response: The grade_items of the course requested
*/
function get_grade_items($course){
	global $config;
	global $routes;

	$route_params = array(
		 'version' => $config['lms_ver']['le'],
		 'orgUnitId' => $course->get_id()
		);

	$response = get($routes['GET_GRADE_ITEMS'], $route_params);
	$items = array();
	foreach($response as $g) {
		if ($g['GradeType'] == 'Numeric') {
			array_push($items, new NumericGradeItem($course, $g));
		}
	}

	return $items;
}

function get_grade_item($course_id, $grade_item_id) {
	global $config;
	global $routes;

	$route_params = array(
		 'version' => $config['lms_ver']['le'],
		 'orgUnitId' => $course_id, 
		 'gradeObjectId' => $grade_item_id
	);

	$response = get($routes['GET_GRADE_ITEM'], $route_params);
	
	return $response;
}

/*
Posts a Grade object to Brightspace using a PUT request

Preconditions:
	grade : the grade to post
Postconditions:
	grade JSON is PUT to Brightspace
*/
function put_grade($grade){
	global $config;
	global $routes;
	
	$route_params = array(
		'version'=> $config['lms_ver']['le'],
		'orgUnitId' => $grade->get_grade_item()->get_course()->get_id(),
		'gradeObjectId' => $grade->get_grade_item()->get_id(),
		'userId' => $grade->get_student()->get_id(),
	);

	$data = $grade->get_json();

	# Make PUT request
	$response = put($routes['SET_GRADE'], $route_params, $data);

	return json_encode($response);

}

function put_grades($grades) {
	$successful = array();
	$failed = array();

	foreach($grades as $grade) {
		try {
			put_grade($grade);
			array_push($successful, $grade);
		}
		catch (Exception $e) {
			$error = array(
				'msg' => $e,
				'grade' => $grade
			);
			array_push($failed, $grade);
		}
	}

	return array($successful, $failed);
}
/*
Posts a GradeItem object to Brightspace using a PUT request

Preconditions:
	grade_item : the grade_item to post
Postconditions:
	grade_item JSON is PUT to Brightspace
*/
function put_grade_item($grade_item){

	global $config;
	global $routes;
	
	$route_params = array(
		'version' => $config['lms_ver']['le'],
		'orgUnitId' => $grade_item->get_course()->get_id(),
		'gradeObjectId' => $grade_item->get_id()
	);

	$data = $grade_item->get_json();
	$to_remove = array('Weight', 'GradeSchemeUrl', 'Id', 'ActivityId', 'AssociatedTool');
	foreach($to_remove as $item) {
		unset($data[$item]);
	}
	$data['Description'] = array(
		'Content' => $data['Description']['Html'],
		'Type' => 'Html'
	);
	
	$response = put($routes['SET_GRADE_ITEM'], $route_params, $data);
	if (isset($response['MaxPoints'])) {
		//can't use response `MaxPoints` since due to api bug, int val returned in response even when decimal set
		return $grade_item->get_max();
	}
	return json_encode($response);
}

/*
Retrieves the collection of users enrolled in the identified org unit.

Preconditions:
	user (Course object) : A Course object to retrieve grades from.

Postconditions:
	returns:
	user_enrollments (dict) : A dict of user_enrollment data corresponding to the given User object.
*/
function get_user_enrollments($user, $roles = array()){

	global $config;
	global $routes;

	$route_params = array(
		'version' => $config['lms_ver']['lp'],
		'userId' => $user->get_id(),
	);

	$response = get($routes['GET_USER_ENROLLMENTS'], $route_params);
	
	$courses = array();
	foreach($response['Items'] as $c) {
		try {
			if ($c['OrgUnit']['Type']['Name'] == 'Course Offering' && (empty($roles) || in_array($c['Role']['Id'], $roles))) {
				array_push($courses, new Course($user, $c));
			}
		}
		catch (Exception $e) {
			//do nothing
		}
	}
	error_log('Extracted ' . sizeof($courses) . ' of ' . sizeof($response['Items']) . ' courses  for ' . $user->get_full_name(), 0);
	return $courses;
}

function get_who_am_i() {
	global $config;
	global $routes;
	
	$route_params = array('version' => $config['lms_ver']['lp']);
	$response = get($routes['GET_WHO_AM_I'], $route_params);
	
	return $response;
}

//TODO: fix how report.php gets grades so can delete this
function get_grade_values($course_id, $grade_item_id) {
	global $config;
	global $routes;
	
	$route_params = array(
		'version' => $config['lms_ver']['le'],
		'orgUnitId' => $course_id,
		'gradeObjectId' => $grade_item_id
	);
	$additional_params = array('pageSize=200');

	$response = get($routes['GET_GRADE_VALUES'], $route_params, $additional_params);
	return $response['Objects'];
}

function get_course_enrollments($course) {
	global $config;
	global $routes;
	
	$route_params = array(
		'version' => $config['lms_ver']['lp'],
		'orgUnitId' => $course->get_id(),
	);
	
		$response = get($routes['GET_COURSE_ENROLLMENTS'], $route_params);
		$members = array();
		foreach($response['Items'] as $m) {
			$members[] = new OrgMember($m);
		}
		return $members;
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

	$decoded_response = json_decode($response, true);
	if ($httpCode != 200) {
		throw new Exception('Valence API call failed: ' . $httpCode . "-" . $route . ': ' . $response);
	}
	
	return $decoded_response;
}
?>
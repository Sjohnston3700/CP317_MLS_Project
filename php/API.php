<?php


	require_once 'Requests.php';
	Requests::register_autoloader();
	
	$SUCCESS = 200;
	$API_ROUTE = '/d2l/api/versions/';
	$GET_GRADES_ROUTE     = '/d2l/api/le/(version)/(orgUnitId)/grades/';
	$SET_GRADE_ROUTE      = '/d2l/api/le/(version)/(orgUnitId)/grades/(gradeObjectId)/values/(userId)';
	$GET_COURSE_MEMBERS   = '/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/';
	$GET_USER_ENROLLMENTS = '/d2l/api/lp/(version)/enrollments/myenrollments/';
	$GET_USER_ENROLLMENT  = '/d2l/api/le/(version)/(orgUnitId)/grades/';
	$GET_WHO_AM_I         = '/d2l/api/lp/(version)/users/whoami';
	
	
	function get($route, $user = NULL, $route_params = array(), $additional_params = array()){
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
		
		$route = update_route($route, $route_params);
		
		if ($user != NULL) {
			$route = $user->get_context()->createAuthenticatedUrl($route, 'GET');
		}
		
		$response = Requests::get($route, $additional_params = payload );
		
		check_request($response);
		
		$results = json_enconde($response);
		
		if (in_array("PagingInfo", results.keys()) == True and $results("PagingInfo")("HasMoreItems") == True){
			$bookmark = $results("PagingInfo")("Bookmark");
			$next_results = get($route, $user, $route_params,("Bookmark"=> $bookmark));    
			$results("Items") = $results("Items") + $next_results("Items");
        }
		
		return $results
	}

	function put($route, $user, $route_params, $params){
		/*
		Uses a PUT request to set JSON
		
		Preconditions :
			grade_item (GradeItem object) : The grade_item to change grade data for
			params (json) : JSON grade data to send
		Postconditions:
			Brightspace data will be updated with params as JSON
		*/
		
		//Make request to PUT grades
		$route = update_route($route, $route_params);
		$response = Requests::put($user->get_context()->createAuthenticatedUrl($route, 'PUT'), $data = $params);
		
		//Check if request was valid
		check_request($response);
		return;
	}
	
	function update_route($route, $params){
    /*
    Function to update api route by replace (...) with the appropriate value
    
    Preconditions: 
        route: the route from the valence docs (eg. '/d2l/api/le/(version)/(orgUnitId)/grades/')
        params: dictionary of replacement values (eg {'version':1.22,'orgUnitId':23456})

    Postconditions:
        Returns new route - Does not check for missed values
    */
	
    if ($params != NULL){
		foreach ($params as $key){
			$temp_string = "(", $key, ")";
			$route = str_replace($temp_string, ((string)($params(key))), $route );
		}
	}
	
	if ((strpos($route, '(')) !== false or (strpos($route, ')')) !== false){	//check for missed stuff to replace
        $exception_message = "Route : ",$route "needs more parameters";
        throw new RuntimeException($exception_message);
	}
    return $route;
	
	}
	
	
	function check_request($request){
    /*
    Function to test if a request was valid.

    Preconditions:
        request : the request object to test
    */
	
    if ((var_dump($request->success)) == False){
		
		/*Line in API.py is:
		exception_message = 'Request returned status code : {}, text : {}'.format(request.status_code,request.text)
		I'm not sure what the equivalent for request.text is in this case
		*/
		$exception_message = "Request returned status code : ",$request->$status_code,", text : ";
        throw new RuntimeException($exception_message);
	}
	
    return;
	
	}
	
	
	function get_grade_items($course){
		$user = $course->get_user();
		$route_params = array("version" => $user->get_host()->get_api_version("le"), "orgUnitId" => $course.get_id());
		$response = get($GET_GRADES_ROUTE, $user, $route_params);
		
		return $response;
	}
	
	
	function put_grade($grade){
    '''
    Posts a Grade object to Brightspace using a PUT request
    
    Preconditions:
        grade : the grade to post
    Postconditions:
        grade JSON is PUT to Brightspace
    '''
    $user = $grade->get_user();
    $route_params = array(
		"version"=> $user->get_host()->get_api_version("le"),
        "orgUnitId" => $grade->get_grade_item()->get_course()->get_id(),
        "gradeObjectId" => $grade->get_grade_item()->get_id(),
        "userId" => $grade->get_student()->get_id() 
	);
		
    $params = array("Comments" => $grade->get_comment(), "PrivateComments" => ""); # For generic Grade
    
    # TODO: Support other Grade types?
    $params("GradeObjectType") = 1; # NumericGrade Type
    $params("PointsNumerator") = $grade->get_value(); # For NumericGrade
    
    # Make PUT request
    $respose = put(SET_GRADE_ROUTE, $user, $route_params, $params);
    
	return;
	
	}
	
	function get_user_enrollments($user){
    /*
    Function to test if a request was valid.

    Preconditions:
        request : the request object to test
    */
	

	
	
	
	}
	
    return;
	
	}
	
	function get_who_am_i($user){
    /*
    Retrieve the current user context’s user information as PHP dict JSON.
    
    Preconditions:
        user : the Course to retrieve grades from
    Postconditions:
        returns
         WhoAmIUser JSON block for the current user context (as python dict)
    */
	
    $route_params = $user->get_host->get_api_version('lP');
	$r = get(GET_USER_ENROLLMENTS, $user, $route_params);
    return;
	}
?>
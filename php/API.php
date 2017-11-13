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
	
	
	function get($route, $user = NULL, $route_params = array()){
		/* 
		Uses a GET request to get JSON

		Preconditions:
			user - A User object corresponding to the current user
			route - The route to make a GET request to
			route_params - A dictionary of parameters corresponding to route
		Postconditions
			On success:
				Returns:
				Python dict of grade objects
			On failure:
				raises RuntimeError
		*/
		
		// For making a call which does not require User context
		if ($user == NULL) {
			$response = Requests::get(update_route($route, $route_params));
		}
		else{
			//Make request to GET grades
			$route = update_route($route, $route_params);
			$response = Requests::get($user->get_context()->createAuthenticatedUrl($route, 'GET'))
		}
		
		//Check if request was valid
		check_request($response);
		return (json_decode($response));
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
		$response = Requests::put($user->get_context()->createAuthenticatedUrl($route, 'PUT'), $data = $params)
		
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
	
    if ($params == NULL){
        return $route;
	}
	
	
    foreach ($params as $key):
		$temp_string = "(", $key, ")";
		$route = str_replace($temp_string, ((string)($params[key])), $route );
    return $route
	
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
?>
<?php
	require_once $_SERVER['DOCUMENT_ROOT'] . '/CP317_MLS_Project/php/root/config.php';
	require_once 'Requests.php';
	require_once $config['libpath'] . '/D2LAppContextFactory.php';
	Requests::register_autoloader();	
	$SUCCESS = 200;
	
	function get($route, $user, $route_params, $additional_params){
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
		
		//Keywords such as true, fase and null must be in lower case 
		if ($user != NULL) {
			$route = $user->get_context()->createAuthenticatedUrl($route, 'GET');
		}
		
		$response = Requests::get($route, $additional_params = payload ); //Control structure issue, no spaces before or after parenthesis
		
		check_request($response);
		
		$results = json_encode($response);
		
		//Keywords such as true, fase and null must all be in lower case 
		if (in_array("PagingInfo", results.keys()) && $results["PagingInfo"]["HasMoreItems"]){
			$bookmark = $results["PagingInfo"]["Bookmark"];
			$next_results = get($route, $user, $route_params, $additional_params = array("Bookmark" => $bookmark));
			
			$results["Items"] = $results["Items"] + $next_results["Items"]; 
        }
		
		return $results;
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
	
	//Keywords such as true, fase and null must be in lower case 
    if ($params != NULL){
		foreach ($params as $key){
			$temp_string = "(" . $key . ")";
			$route = str_replace($temp_string, ((string)($params(key))), $route ); //Control structure issue, no spaces before or after parenthesis
		}
	}
	
	if ((strpos($route, '(')) !== false or (strpos($route, ')')) !== false){	//check for missed stuff to replace
        $exception_message = "Route : " . $route . "needs more parameters";
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

		if (!(var_dump($request->success))) { //Keywords such as true, fase and null must be in lower case 

			/*Line in API.py is:
			exception_message = 'Request returned status code : {}, text : {}'.format(request.status_code,request.text)
			I'm not sure what the equivalent for request.text is in this case
			*/
			$exception_message = "Request returned status code : " . $request->$status_code . ", text : "; 
			throw new RuntimeException($exception_message);
		}
	
	}
	
	
	function get_grade_items($course){
		$user = $course->get_user();
		$route_params = array("version" => $user->get_host()->get_api_version("le"), "orgUnitId" => $course.get_id());
		$response = get($GET_GRADES_ROUTE, $user, $route_params);
		
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
		$user = $grade->get_user();
		$route_params = array(
			"version"=> $user->get_host()->get_api_version("le"),
			"orgUnitId" => $grade->get_grade_item()->get_course()->get_id(),
			"gradeObjectId" => $grade->get_grade_item()->get_id(),
			"userId" => $grade->get_student()->get_id(),
		);

		$params = array("Comments" => $grade->get_comment(), "PrivateComments" => ""); # For generic Grade

		# TODO: Support other Grade types?
		$params["GradeObjectType"] = 1; # NumericGrade Type
		$params["PointsNumerator"] = $grade->get_value(); # For NumericGrade

		# Make PUT request
		$respose = put($SET_GRADE_ROUTE, $user, $route_params, $params);

		return;
	
	}
	
	function put_grade_item($grade_item){
		/*
		Posts a GradeItem object to Brightspace using a PUT request

		Preconditions:
			grade_item : the grade_item to post
		Postconditions:
			grade_item JSON is PUT to Brightspace
		*/

		$user = $grade_item->get_user();
		$route_params = array(
			"version" => $user->get_host()->get_api_version("le"),
			"orgUnitId" => $grade->get_grade_item()->get_course()->get_id(),
			"gradeObjectId" => $grade->get_grade_item()->get_id(),
		);
		$params = array(
			"MaxPoints" => $grade_item->get_max(), 
			"CanExceedMaxPoints" => $grade_item->can_exceed(), 
			"GradeType" => "Numeric",
		);
		$response = put($SET_GRADEITEM_ROUTE, $user, $route_params, $params);

	}
	
	
	function get_user_enrollments($user){
	   /*
		Retrieves the collection of users enrolled in the identified org unit.

		Preconditions:
			user (Course object) : A Course object to retrieve grades from.

		Postconditions:
			returns:
			user_enrollments (dict) : A dict of user_enrollment data corresponding to the given User object.
		*/
	
		$route_params = array(
			"version" => ($user->get_host()->get_api_version("lp")),
			"userId" => $user->get_id(),
			);

		$response = get($GET_USER_ENROLLMENTS, $user, $route_params);
		$user_enrollments = $response("Items");
		return user_enrollments;
	
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
		global $routes;
		global $config;
		
		
		$route = $routes['BASE_URL'] . '/d2l/api/lp/' . $config['LP_Version'] . '/users/whoami';
		$verb = 'GET';
		
	  	$userId = $_SESSION['userId'];
    	$userKey = $_SESSION['userKey'];
		
		// Create authContext
		$authContextFactory = new D2LAppContextFactory();
		$authContext = $authContextFactory->createSecurityContext($config['appId'], $config['appKey']);
		
		// Create userContext
		$hostSpec = new D2LHostSpec($config['lms_host'], $config['lms_port'], $config['scheme']);
		$userContext = $authContext->createUserContextFromHostSpec($hostSpec, $userId, $userKey);
		
		// Create url for API call
		$uri = $userContext->createAuthenticatedUri($route, $verb);
		$uri = str_replace(':443', '', $uri);
		echo $uri;
		
		// Setup cURL
		$ch = curl_init();
		$options = array(
			CURLOPT_RETURNTRANSFER => true,
			CURLOPT_CUSTOMREQUEST  => $verb,
			CURLOPT_URL            => $uri,
			CURLOPT_SSL_VERIFYPEER => true,
			CURLINFO_HEADER_OUT => true
		);
		

		curl_setopt_array($ch, $options);
		
		$response = curl_exec($ch);
		$httpCode  = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		$contentType = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
		$responseCode = $userContext->handleResult($response, $httpCode, $contentType);
		if ($responseCode == D2LUserContext::RESULT_OKAY) {
			return json_decode($response, true);
		}
		
		$errors = curl_error($ch);
		curl_close($ch);
		var_dump($errors);
		var_dump($response);
		echo '<br> Response code: ' . $responseCode;
		throw new Exception("Valence API call failed: $httpCode: $response");

	}
?>
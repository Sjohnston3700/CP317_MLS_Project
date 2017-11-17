<?php
	
	include 'API.php';
	include 'Course.php'; //Required in the user construct, though not present in the python version?
	
	class OrgMember {
		/*
		Instantiates a new OrgMember object 
		Preconditions:
			$org_member_params: Parameters to init this user (dict)
		*/
		function __construct($org_member_params) {
			$this->name = $org_member_params['User']['DisplayName'];
			$this->id = $org_member_params['User']['Identifier'];
			$this->org_id = $org_member_params['User']['OrgDefinedId'];
			$this->role = $org_member_params['Role']['Id'];
		}
		/*
		Postconditions:
			returns
			The name of the OrgMember (str)
		*/
		function get_name() {
			return $this->name;
		}
		/*
		Postconditions:
			returns
			The Brightspace ID of the OrgMember (str)
		*/
		function get_id() {
			return $this->id;
		}
		/*
		Postconditions:
			returns
			The organization defined ID of the OrgMember (str)
		*/
		function get_org_id() {
			return $this->org_id;
		}
		/*
		Postconditions:
			returns
			The role id of the OrgMember (str)
		*/
		function get_role() {
			return $this->role;
		}
	}
	
	class User {
		/*
		Instantiates a new User object
		Preconditions:
			$context: The Brightspace User context ()
			$host: The Host object corresponding to the user (Host)
			$roles: List of roles, default: None (list)
		*/
		function __construct($context, $host, $roles=[]) {
			$this->context = $context;
			$this->host = $host;
			$me = API->get_who_am_i(host); //Syntax error, unexpteced use of -> 
			$fName = $me['FirstName'];
			$lName = $me['LastName'];
			$this->name = "$fName $lName";
			$this->id = '';
			foreach(API->get_user_enrollments() as $item) { //Syntax error, unexpteced use of -> 
				if (in_array($item['Access']['ClasslistRoleName'], $roles)) {
					$this->courses = new Course($item);
				}
			}
		}
		/*
		Returns a copy of the list of courses the user has access to
		Postconditions:
			returns
			Copy of a python list of all courses accessible by this user
			*/
		function get_courses() {
			$copy = array();
			foreach($this->courses as $i => $j) {
				$copy[$i] = clone $v;
			}
			return $copy;
		}
		/*
		Returns a single course with id matching the given id, None if this User does not have access to the course
		Preconditions:
			id - ID of the course (str or int)
		Postconditions
			returns
			A single course object with matching id, None if this User cannot access that course
		*/
		function get_course($id) {
			foreach($this->courses as $course) {
				if($course->get_id == $id) {
					return $course;
				}
			}
			return NULL;
		}
		/*
		Returns the user context belonging to this user
		Postconditions:
			returns
			A Brightspace user context
		*/
		function get_context() {
			return $this->context;
		}
		/*
		Gets the host being used by this User
		Postconditions:
			returns 
			A Host object
		*/
		function get_host() {
			return $this->host;
		}
	}
<?php
	
	include 'copy.php';
	include 'API.php';
	
	class OrgMember {
		function __construct($org_member_params) {
			"""
			Instantiates a new OrgMember object 
			Preconditions:
				org_member_params: Parameters to init this user (dict)
			"""
			$this->name = $org_member_params['User']['DisplayName'];
			$this->id = $org_member_params['User']['Identifier'];
			$this->org_id = $org_member_params['User']['OrgDefinedId'];
			$this->role = $org_member_params['Role']['Id'];
		}
		
		function get_name() {
			"""
			Postconditions:
				returns
				The name of the OrgMember (str)
			"""
			return $this->name;
		}
		function get_id() {
			"""
			Postconditions:
				returns
				The Brightspace ID of the OrgMember (str)
			"""
			return $this->id;
		}
		function get_org_id() {
			"""
			Postconditions:
				returns
				The organization defined ID of the OrgMember (str)
			"""
			return $this->org_id;
		}
		function get_role() {
			"""
			Postconditions:
				returns
				The role id of the OrgMember (str)
			"""
			return $this->role;
		}
	}
	
	class User {
		function __construct($context, $host, $roles=[]) {
			"""
			Instantiates a new User object
			Preconditions:
				context: The Brightspace User context ()
				host: The Host object corresponding to the user (Host)
				roles: List of roles, default: None (list)
			"""
			$this->context = $context;
			$this->host = $host;
			
			//TO EDIT
		}
		function get_courses() {
			"""
			Returns a copy of the list of courses the user has access to
		
			Postconditions:
				returns
				Copy of a python list of all courses accessible by this user
			"""
			//TO EDIT
		}
		function get_course($id) {
			"""
			Returns a single course with id matching the given id, None if this 
			User does not have access to the course
		
			Preconditions:
				id - ID of the course (str or int)
			Postconditions
				returns
				A single course object with matching id, None if this User cannot access that course
			"""
			foreach($this->courses as $course) {
				if($course->get_id == $id) {
					return $course;
				}
			}
			return NULL;
		}
		function get_context() {
			"""
			Returns the user context belonging to this user
		
			Postconditions:
				returns
				A Brightspace user context
			"""
			return $this->context;
		}
		function get_host() {
			"""
			Gets the host being used by this User
		
			Postconditions:
				returns 
				A Host object
			"""
			return $this->host;
		}
	}
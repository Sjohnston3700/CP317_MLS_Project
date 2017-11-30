<?php
	
	require_once 'API.php';
	require_once 'Course.php'; //Required in the user construct, though not present in the python version?
	
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
	
	class User extends OrgMember{
		/*
		Instantiates a new User object
		Preconditions:
			$context: The Brightspace User context ()
			$host: The Host object corresponding to the user (Host)
			$roles: List of roles, default: None (list)
		*/
		function __construct($roles) {
			$this->roles = $roles;
			$this->json = get_who_am_i();
			$this->id = $me['Identifier'];
			$this->courses = $this->get_course();
		}
		/*
		Get First Name  (Getter)
		Postconditions
			returns
			first_name - This object's first name
		*/
		function get_first_name() {
			return $this->json['FirstName'];
		}
		/*
		Get Last Name  (Getter)
		Postconditions
			returns
			last_name - This object's last name
		*/
		function get_last_name() {
			return $this->json['LastName'];
		}
		/*
		Get ID function (Getter)
		Postconditions
			returns
			id - this object's id
		*/
		function get_id() {
			return $this->id;
		}
		/*
		Get Name function (getter)
		Postconditions
			returns
			name - the object's full name
		*/
		function get_name() {
			$fname = $this->get_first_name();
			$lname = $this->get_last_name();
			return "$fname $lname";
		}
		/*
		Get Context function (getter)
		Postconditions
			returns
			context - the object's context
		*/
		function get_context() {
			return $this->context;
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
				if($course->get_id() == $id) {
					return $course;
				}
			}
			return null; 
		}
		/*
		Returns a copy of the list of courses the user has access to
		Postconditions:
			returns
			Copy of a python list of all courses accessible by this user
			*/
		function get_courses() {
			return $this->courses;
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
		/*
		Gets the courses dictionary
		Postconditions:
			courses - dictionary of courses
		*/
#		function _get_courses() {
#			$courses = array();
#			foreach(get_user_enrollments($this) as $course) {
#				if (in_array($course['Role']['Id'], $this->roles)) { // This is temp to make loading time quicker for development
#					$courses[] = new Course($this, $course);
#				}
#				
#			}
#			return $courses;
#		}
	}
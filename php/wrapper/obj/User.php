<?php

require_once 'API.php';
require_once 'Course.php';

class User {
    private $context;
    private $json;
    private $courses;


		/*
		Instantiates a new User object
		Preconditions:
			$context: The Brightspace User context ()
			$host: The Host object corresponding to the user (Host)
			$roles: List of roles, default: None (list)
		*/
		function __construct($roles) {

            try {
                $this->json = get_who_am_i();
                $this->courses = get_user_enrollments($this, $roles);
            }
            catch (Exception $e) {
                error_log('Something went wrong. Unable to create User object', 0);
                throw $e;
            }

			$this->roles = $roles;
		}

		function get_roles() {
			return $this->roles;
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
		Get ID function (Getter)
		Postconditions
			returns
			id - this object's id
		*/
		function get_id() {
			return $this->json['Identifier'];
        }
        
        function get_first_name() {
            return $this->json['FirstName'];
        }

        function get_last_name() {
            return $this->json['LastName'];
        }

		/*
		Get Full Name  (Getter)
		Postconditions
			returns
			full_name - This object's full_name
		*/
		function get_full_name() {
			return $this->get_first_name() . ' ' . $this->get_last_name();
		}
    }
    
?>
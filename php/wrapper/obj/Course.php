<?php
	require_once 'API.php';
	require_once 'GradeItem.php';
	require_once 'OrgMember.php';
	
	class Course {
		private $json;
		private $user;
		private $grade_items;
		private $members;

		/*
	user (user object) - info about user
	course_params - info about course (Enrollment.MyOrgUnitInfo) 
	*/
		function __construct ($user, $course_params) {
			$this->json = $course_params;
			$this->user = $user;
			$this->grade_items = get_grade_items($this);
			$this->members = get_course_enrollments($this);
		}

		function get_json() {
			return $this->json;
		}

		/*
		Function will return all the current members for current course
		return:
			result - list
		*/
		
		/*
		Function will return all the current grade object (Numeric) for current course
		return:
			grade_items - list
		*/
		function get_grade_items() {
			return $this->grade_items;
		}
		/*
		Function will return specific grade item for the given id
		return:
			grade_item or NULL
		*/
		function get_grade_item($id) {
			foreach($this->grade_items as $grade_item) {
				if((string)($grade_item->get_id()) == (string) $id) {
					return [$grade_item][0]; //TODO: try w/o [0] - don't know why there
				}
			}	
			return null;			
		}
		/*
		Function will return the name of course
		PostCondition:
			return $this.name - current course name
		*/
		function get_name() {
			return $this->json['OrgUnit']['Name'];
		}
		/*
		Function will return the id for the current course
		PostCondition:
			return $this.id - id for the current course
		*/
		function get_id() {
			return $this->json['OrgUnit']['Id'];
		}
		/*
		Function will return the user object
		PostCondition:
            return self._user - user 
		*/
		function get_user() {
			return $this->user;
		}
		/*
		Function will return all the users for the current course
		PostCondition:
			return list of Orgmembers
		*/
		function get_members($role = array()) {
			if (empty($role) == false) {
				$items = array();
				foreach($this->members as $member) {
					if (in_array($member->get_role(),$role)) {
						array_push($items,$member);
					}
				}
				return $items;
			}
			return $this->members;
		}
		/*
		Function will return the member request if it exist, 
		Otherwise, it return None
		*/
		function get_member($id, $roles = array()) {
			foreach ($this->members as $member) {
				if($member->get_id() == $id) {
					if (empty($roles) || in_array($member->get_role(), $roles)) {
						return $member;
					}
					return null;
				}
			}
			return null;
		}
	}
?>
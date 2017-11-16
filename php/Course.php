<?php

	include 'API.php';
	include 'GradeItem.php';
	include 'OrgMember.php';

	$GET_GRADE_ITEMS = "/d2l/api/le/(version)/(orgUnitId)/grades/";
	$GET_MEMBERS = "/d2l/api/lp/(version)/enrollments/orgUnits/(orgUnitId)/users/"

	class Course {
		function __construct ($user,$course_params) {
			$this->user = $user;
			$this->name = $course_params['OrgUnit']['Name'];
			$this->id = $course_params['OrgUnit']['Id'];
			$this->user_role = $course_params['Access']['ClasslistRoleName'];
			$this->grade_items = $this->_get_grade_items();
			$this->members = [OrgMember($member) foreach(API->get($GET_MEMBERS,$user,array('orgUnitID'=>$this->id)['Items'] as $member))]
		}
		function _get_grade_items() {
			$gradeitems = API->get($GET_GRADE_ITEMS, $this->user, array('orgUnitId'=>$this->id));
			$items = array();
			foreach($gradeitems as $item) {
				if ($item['GradeType'] == 'Numeric') {
					$items::append(NumericGradeItem($item));
				}
			}
			return $items;
		}
		function get_grade_items() {
			"""
			Function will return all the current grade object (Numeric) for current course
			return:
            Gradeitems - list
			"""
			return $this->grade_items;
		}
		function get_grade_item($id) {
			try {
				return [$grade_item foreach($this->grade_items) if str($grade_item->get_id()) == str($id)][0] 
			} catch (Exception $e) {
				return NULL;
			}
			
		}
		function get_name() {
			"""
			Function will return the name of course
			PostCondition:
            return self.name - current course name
			"""
			return $this->name;
		}
		function get_id() {
			"""
			Function will return the id for the current course
			PostCondition:
            reutrn self.id - Id for the current course
			"""
			return $this->id;
		}
		function get_user_role() {
			"""
			Function will return the user fole for current course
			PostCondition:
            reutrn self.user_role - user role for current course
			"""
			return $this->user_role;
		}
		function get_members($role = []) {
			if ($role != []) {
				$items = array();
				foreach($this->members as $member) {
					if (in_array($member->get_user_role, $role)) {
						$items::append($member);
					}
				}
				return $items;
			}
			return $this->members;
		}
		function get_member($org_id) {
			"""
			Function will return the member request if it exist, 
			Otherwise, it return None
			"""
			foreach ($this->members as $member) {
				if($member->get_org_id() == $org_id) {
					return $member;
				}
			}
			return NULL;
		}
		function get_user() {
			"""
			Function will return the user object
			PostCondition:
            return self._user - user 
			"""
			return $this->user
		}
	}
?>
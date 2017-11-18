<?php

	include 'API.php';
	include 'GradeItem.php';
	include 'OrgMember.php';
	include 'routes.php';


	class Course {

		/*
		user (user object) - info about user
		course_params - info about course (Enrollment.MyOrgUnitInfo) 
		*/
		function __construct ($user, $course_params) {
			$this->user = $user;
			$this->name = $course_params['OrgUnit']['Name'];
			$this->id = $course_params['OrgUnit']['Id'];
			$this->user_role = $course_params['Access']['ClasslistRoleName'];
			$this->grade_items = $this->_get_grade_items();
			$members = array();
			foreach(get($GET_MEMBERS,$user,array('orgUnitID'=>$this->id))['Items'] as $member) {
				array_push($members,$member);
			}
			$this->members = $members;
			
			//[OrgMember($member) foreach(API-($GET_MEMBERS,$user,array('orgUnitID'=>$this->id)['Items'] as $member))];
		}
		/*
		Function will return list of grade items
		return :
            lists - grade item
		*/
		function _get_grade_items() {
			$gradeitems = get($GET_GRADE_ITEMS, $this->user, array('orgUnitId'=>$this->id));
			$items = array();
			foreach($gradeitems as $item) {
				if ($item['GradeType'] == 'Numeric') {
					array_push($items,(NumericGradeItem($this, $item)));
				}
			}
			return $items;
		}
		/*
		Function will return all the current grade object (Numeric) for current course
		return:
			Gradeitems - list
		*/
		function get_grade_items() {
			return $this->grade_items;
		}
		/*
		Function will return specific grade item for the given id
		return:
			gradeitem or NULL
		*/
		function get_grade_item($id) {
			try {
				foreach($this->grade_items as $grade_item) {
					if(string($grade_item->get_id()) == string($id)) {
						return [$grade_item][0];
					}
				}	
			} catch (Exception $e) {
				return null;
			}
			
		}
		/*
		Function will return the name of course
		PostCondition:
			return self.name - current course name
		*/
		function get_name() {
			return $this->name;
		}
		/*
		Function will return the id for the current course
		PostCondition:
			reutrn self.id - Id for the current course
		*/
		function get_id() {
			return $this->id;
		}
		/*
		Function will return the user fole for current course
		PostCondition:
            reutrn self.user_role - user role for current course
		*/
		function get_user_role() {
			return $this->user_role;
		}
		/*
		Function will return all the users for the current course
		return :
			list of Orgmembers
		*/
		function get_members($role = array()) {
			if (empty($role)) {
				$items = array();
				foreach($this->members as $member) {
					if (in_array($member->get_user_role, $role)) {
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
		function get_member($org_id) {
			foreach ($this->members as $member) {
				if($member->get_org_id() == $org_id) {
					return $member;
				}
			}
			return NULL;
		}
		/*
		Function will return the user object
		PostCondition:
            return self._user - user 
		*/
		function get_user() {
			return $this->user
		}
	}
?>
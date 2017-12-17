<?php
	
	require_once 'API.php';
	require_once 'Course.php'; //Required in the user construct, though not present in the python version?
	
	class OrgMember {
		private $json;

		/*
		Instantiates a new OrgMember object 
		Preconditions:
			$org_member_params: Parameters to init this user (dict)
		*/
		function __construct($org_member_params) {
			$this->json = $org_member_params;
		}

		function get_json() {
			return $this->json;
		}

		/*
		Postconditions:
			returns
			The name of the OrgMember (str)
		*/
		function get_name() {
			return $this->json['User']['DisplayName'];
		}
		/*
		Postconditions:
			returns
			The Brightspace ID of the OrgMember (str)
		*/
		function get_id() {
			return $this->json['User']['Identifier'];
		}
		/*
		Postconditions:
			returns
			The organization defined ID of the OrgMember (str)
		*/
		function get_org_id() {
			return $this->json['User']['OrgDefinedId'];
		}
		/*
		Postconditions:
			returns
			The role id of the OrgMember (str)
		*/
		function get_role() {
			return $this->json['Role']['Id'];
		}
	}

?>
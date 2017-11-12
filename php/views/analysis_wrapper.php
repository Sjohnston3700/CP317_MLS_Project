<html>
	<head>
		<title>Wrapper - Analysis</title>
	</head>
	<body>
		<script src="../../python/static/js/toc_generator.js"></script>
		<h1>Brightspace API Python Wrapper - Analysis</h1>
		<p>Version 1.0</p>
		<p>Last updated: October 23, 2017</p>
		
		<div id="toc">
			<h2>Table of Contents</h2>
		</div>

		<h2>Introduction</h2>
		<p>
      	  The Brightspace API Wrapper is a library used to make calls to the Brightspace API. It allows developers to fetch and push information through the API in a friendly manner. Rather than directly making HTTP requests, developers can simply use the functions available in the wrapper's library. This wrapper is being developed primarily for ezMarker, a web application for uploading grades and feedback to a Brightspace environment. PHP and Python versions of the wrapper are being developed to support the corresponding versions of ezMarker. This document outlines the structure of the classes and objects for the Brightspace API Wrapper application.
    	</p>


		<h2>Object Classification</h2>
		<h3>Objects Diagram</h3>
		<img class="prototype-img" src="../../python/static/img/wrapper_analysis_object_diagram.png" />

		<h3>Entity Objects</h3>
		<ul>
			<li>Host - Store information about the connection, including the Internet Protocol and API version.</li>
			<li>User - Stores information about logged in user, including the user's identity and permissions.</li>
			<li>Course - Stores information about a course, which may consist the course identification code, professor, registerated students, and course content.</li>
			<li>GradeItem - Stores information about a grade item's parameters, including the outline and grading type. Implemented by specific grade item type.</li>
			<li>Grade - Stores information about a specific grade, unique to the grade item's grading scale. Implemented by specific grade type.</li>
			<li>OrgMember - Stores information about a a member of the organization. More specifically a student, their coursework and grades. </li>
		</ul>
		
		<h3>Boundary Objects</h3>
		<p>The Brightspace API Wrapper does not have any boundary objects specifically in its own scope. Its calling applications are the boundary object(s).</p>

		<h3>Control Objects</h3>
		<ul>
			<li>API - Interacts with Brightspace server.</li>
		</ul>
		<p>The rest of the entity objects have their own respective control objects to parse and dispatch information.</p>

		<h2>Class Diagram</h2>
		<img src="../../python/static/img/wrapper_analysis_class_diagram.jpg">

		<h2 id="toc_exclude">Revision History</h2>
		<h3 id="toc_exclude">Version 1.0 - 10/23/2017</h3>

		<p>Authors: Sarah Johnston, Troy Nechanicky, Hind Althabi</p>
        <h3 id="toc_exclude">Version 2.0 - 11/4/2017</h3>
        <ul><li> Added control objects to objects diagram </li></ul>
        <p>Authors: Hind Althabi</p>
     
		<h3 id="toc_exclude">Version 3.0 - 11/11/2017</h3>
        <ul><li> Updated in accordance to changes made in Design document</li></ul>
        <p>Authors: Tyler Gwynn, Troy Nechanicky</p>
	
	</body>
</html>
<style>
	img {
		width: 800px;
	}

</style>


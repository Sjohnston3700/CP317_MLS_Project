
<head>
	<title>ezMarker - Analysis</title>
</head>
<body>
	<script src="../../python/static/js/toc_generator.js"></script>

	<h1>ezMarker - Analysis</h1>
	<p>Version 2.0</p>
	<p>Last updated: October 22, 2017</p>

	<div id="toc">
		<h2>Table of Contents</h2>
	</div>

	<h2>Introduction</h2>
	<p>
		ezMarker is a web application that allows instructors at Wilfrid Laurier University to bulk upload grades and feedback into MyLearningSpace,with the integration of the Brightspace API supported by D2L. The goal of ezMarker is to solve the issues regarding inefficient manual grade uploading and and feedback through the current MyLearningSpace interface. On average, it can take markers a few hours to physically upload grades for one class. Marking time is cut down to minutes with the use of ezMarker's bulk file uploading features. This document outlines the structure of the classes and objects for the ezMarker application, including the software interaction summary.
	</p>

	<hr>

	<h2>Object Classification</h2>

	<h3>Object Diagram</h3>
	<img src="../../python/static/img/object_diagram.png" alt="ezMarker Object Diagram">

	<h3>Entity Objects</h3>
	<ul>
		<li>User - Stores information about logged in user, including the user's identity and permissions.</li>
		<li>Course - Stores information about a course, which may consist the course identification code, professor, registerated students, and course content.</li>
		<li>Student - Stores information about a student, specifically their coursework and grades. </li>
		<li>GradeItem - Stores information about a grade item's parameters, including the outline and grading type. Implemented by specific grade item type.</li>
		<li>Grade - Stores information about a specific grade, unique to the grade item's grading scale. Implemented by specific grade type.</li>
	</ul>

	<h3>Boundary Objects</h3>
	<ul>
		<li>LoginView - Where user signs in with MLS credentials and receives Brightspace API token.</li>
		<li>LogoutView - Where user signs out. The user is also presented with the choice to log back in with a link back to the LoginView.</li>
		<li>CourseListView - Where user gets a list of courses that they have permission to manage grades.</li>
		<li>SearchStudentsView - Where user can search for students. The search functions are either by name or student identificaton number.</li>
		<li>AvailableGradeItemsView - Where user selects a grade item of a course that they have permission to upload grades to.</li>
		<li>ChangeGradeTotalView - Where user can change the grade total for a grade item.</li>
		<li>ManualGradingView - Where user can manually input grades for a set of students.</li>
		<li>BulkGradingView - Where user can upload a file for bulk grade submission.</li>
		<li>ReportView - Where user will be shown how many grades were successfully set and if any errors occurred.</li>
	</ul>

	<h3>Control Objects</h3>
	<ul>
		<li>LoginController - Handles retrieval of Brightspace token and updating the User object.</li>
		<li>LogoutController - Handles the user's signout process and updating User object.</li>
		<li>CourseListController - Allows retrieval of courses that the user has permission to upload grades to.</li>
		<li>SearchStudentsController - Allows searching of students by name or student ID.</li>
		<li>AvailableGradeItemsController - Allows retrieval of a course's GradeItems that the user has permission to upload grades to.</li>
		<li>ChangeGradeTotalController - Allows changing of the grade total of a grade item and updating GradeItem object.</li>
		<li>GradingController - Handles  parsing, validating and uploading of students' grades and updating GradeItem object.</li>
	</ul>

	<h2>Class Diagram</h2>
	<p>Please refer to Section 3 of the analysis document for the Brightspace API Python Wrapper.</p>

	<h2 id="toc_exclude">Revision History</h2>
	<h3 id="toc_exclude">Version 1.0 - 10/16/2017</h3>

	<p>Authors: Sumeet Jhand, Shuaib Reeyaz, Sarah Johnston</p>
	<p>SQA: Harold Hodgins, Troy Nechanicky</p>

	<h3 id="toc_exclude">Version 2.0 - 10/22/2017</h3>
	<h4 id="toc_exclude">Revision Notes</h4>
	<ul>
		<li>Removed the use of "coordinates"</li>
		<li>Added object description details</li>
	</ul>	
	<p>Authors: </p>
	<p>SQA: Sophie Wang, Pirajeev Prabaharan</p>


</body>

<style>
	img 
	{
		width: 1100px;
	}
</style>


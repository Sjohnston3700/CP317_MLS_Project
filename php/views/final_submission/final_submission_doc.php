<h1>CP317 Fall 2017 - ezMarker Final Submission Document</h1>

<h2>Overview</h2>
<p>
	The ezMarker project has been completed within the deadline specified by the client. The initial goal of this project was to make a web application that allows instructors at Wilfrid Laurier University to bulk upload grades and feedback into MyLearningSpace, with the integration of the Brightspace API supported by D2L. This document summarizes the end product and how it is packaged for the client.
</p>

<h2>Final Submission Contents</h2>
<p>
	The final submission for ezMarker is in four different packages: <strong>PHP ezMarker, PHP Wrapper, Python ezMarker, Python Wrapper</strong>. All packages are as similar as possible, disregarding any barriers due to the programming language used. The Python submission can be found <a href="http://ezmarker.herokuapp.com">here</a> and the PHP submission can be found <a href="http://somethingdumb.ca/index.php?page=final_submission">here</a>. The contents of the final submission include: 
	<ul>
		<li>Brightspace Wrapper</li>
		<ul>
			<li>Configuration file (Host information and API version)</li>
			<li>Classes that contain attributes aligning with the Brightspace API</li>
			<li>Gerenal get and put functions that will work for any valid Brightspace API route</li>
		</ul>
		<li>ezMarker</li>
		<ul>
			<li>Manual grade upload to MLS</li>
			<li>Batch grade upload by CSV to MLS</li>
			<li>Summary report following grade upload</li>
			<li>PHP/Python endpoint files to handle getting data from Brightspace Wrapper</li>
			<li>CSS and JS files to handle user experience</li>
		</ul>
		<li>Documents</li>
		<ul>
			<li>SPMP</li>
			<li>ezMarker Requirements</li>
			<li>ezMarker Analysis</li>
			<li>ezMarker Design</li>
			<li>Wrapper Requirements</li>
			<li>Wrapper Analysis</li>
			<li>Wrapper Design</li>
		</ul>
		<li>Log files</li>
		<ul>
			<li>Git logs</li>
			<li>SQA logs</li>
			<li>Hour logs</li>
		</ul>
	</ul>
</p>

<h2>Issues During Development</h2>
<p>
	Throughout development, there were small details of the product that were not completed by their specified deadlines. The Requirement Document had to be updated accordingly to account for these changes. The group had to reorganize and shift priority of tasks. Some problems encountered during development included: 
		<li>PHP backend development was slower than Python due to: </li>
		<ul>
			<li>the majority of the group not having previous experience in PHP</li>
			<li>some team members producing code with syntax errors and not testing it</li>
		</ul>	
		<li>Unit testing was not completed as planned due to: </li>
		<ul>
			<li>the majority of the group not having previous experience in unit testing</li>
			<li>difficulties in setting up a "mock" user for the Brightspace API</li>
		</ul>
		<li>Team members redoing working code due to: </li>
		<ul>
			<li>lack of communication</li>
		</ul>
		<li>Frontend changes working for one language but breaking it for another due to: </li>
		<ul>
			<li>lack of communication</li>
			<li>lack of testing</li>
			<li>lack of branching in repository</li>
			<li>absense of unit testing</li>
		</ul>
	To combat these issues, the group could have:
	<ul>
		<li>had more regular meetings</li>
		<li>used branching in the repository and only allowed a group of people to push to master</li>
		<li>followed SQA tickets more regilously rather than doing random tasks</li>
		<li>tested ALL code before pushing to the repository</li>
	</ul>

</p>
<h2>Agreement During Development</h2>
<p>
	Although small things went wrong during development, many issues were combatted well by the group. Highlights during development included: 
		<li>Documents were done ahead of schedule to allow for more development time</li>
		<li>Documents were updated throughout the life cycle of the project</li>
		<li>SQA team submitted tickets when necessary</li>
		<li>Many members readily stepped up to sign up for tasks</li>
		<li>Many members that were assigned a task generally completed the task</li>
		<li>Frontend development was completed cleanly (CSS and JS organized and separated from HTML files)</li>
		<li>Backend development successfully integrated with the Brightspace API</li>
		<li>Most code was documented well</li>
		<li>Python and PHP groups talked regularly to keep the two projects in-line</li>
		<li>Little to no code was duplicated among the projects (the same frontend was used for PHP and Python)</li>
</p>
<h2>Incomplete Portions of Submission</h2>
<p>
	Everything except for unit testing was completed for the final submission of the project. Had more time been given, the group could have continued to expand on error prevention and error checking and completed unit testing.
</p>
<h2>Conclsion</h2>
<p>
	In conclusion, the team members had good and poor parts of development. We thank our client for his feedback during the process and hope he enjoys the final submission, with his final charge being FREE!
</p>

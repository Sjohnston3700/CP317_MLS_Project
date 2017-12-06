<html>
    
    <head>
        <title>ezMarker - Help Document</title>
    </head>
    <body>
        <script src="<?=$PATH_TO_STATIC?>/js/toc_generator.js"></script>
        <h1>ezMarker - Help</h1>
        <p>Version 3.0</p>
        <p>Last updated: December 5, 2017</p>
        
        <div id="toc">
            <h2>Table of Contents</h2>
        </div>
        
        <h2>Introduction</h2>
        <p>
         ezMarker is a web application that allows instructors at Wilfrid Laurier University to bulk upload grades and feedback into MyLearningSpace, with the integration of the Brightspace API supported by D2L. The goal of ezMarker is to solve the issues regarding inefficient manual grade uploading through the current MyLearningSpace interface. On average, it can take markers a few hours to manually upload grades for one class. Marking time is cut down to minutes with the use of ezMarker's bulk file uploading.
		</p>
        
        <h2>Login Page</h2>
        
		<p>In order to login, the user needs to have MyLearningSpace credentials.</p>
		<img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/brightspace_login.png">
		<p>If login is unsuccessful, the user is be shown an error message, and needs to retry.</p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/login_failed.png">
		

        <h2>Course List Page</h2>
        <p>After login, a user is presented with a list of courses that they have premission to access and upload grades to it.</p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/course_list_page.png">

        <p>To modify a specific course, the user must select that course and expand it to shows the course's grade items.</p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/grade_items.png">
        
        <h2>Grade Item page</h2>
        <p>
			Once the user selects a grade item, they are redirected to the grade item page. This page allows the user to <strong>update the course maximum</strong>,
			<strong>upload an Autograder file</strong>, or <strong>upload grades manually</strong>.
		</p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/grade_items_page.png">
        
        <h3>Update Maximum Grade</h3>
        <p>
			The user can update the grade item's maximum grade value by entering a positive number and submitting the form with Update Grade Maximum button. 
		</p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/update_grade_max.png">
        <p>When the user submits the form, a message appears to confirm the user wants to proceed.</p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/confirm_update_max.png">
         <p> </p>
        <p>If the user confirms and they submit a valid grade maximum, a success message will appear and the UI will be updated appropriately.</p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/update_max_success.png">
        
        <p>Note:</p>
        <ul>
           <li>If an invalid grade maximum is given, an error message will appear and the user will have to check their input.</li>
         <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/update_max_error.png">
         </ul>
        
        <h3>Automated Upload</h3>
        
        <p>
			The user is prompted to choose a file to upload that follows the Autograder file format of <strong>brightspace_id, grade, name, comment</strong>. 
		
		</p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/automated_upload.png">
        <p>
			If the file is valid and grades are uploaded through the Brightspace API, the user is brought to the report page. Otherwise, they will be shown an error message. If the file is valid but some of the marks are not good, a pop-up will appear to give the user a chance to correct the errors and re-submit. 
		</p>
		<img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/automated_upload_error.png">
		
        <h3>Manual Upoad</h3>
        <p>
			The user can also upload grades manually. Start by searching by student name or Laurier ID in the the search provided. There is a select all button for quickly adding input boxes for all students.
		</p>
         <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/manual_upload.png">
    
        <p>
			The grade is required and must be a positive number. Some grade items allow for the grade to exceed the maximum grade value, while others do not. The 
			comment is not required. 
		</p>
		<p>
			If there are any errors with the user's upload, a pop-up will appear with warning and error messages. The user must fix these issues and re-submit, otherwise 
			cancel their upload. If a warning message appears saying the grade exceeds the grade item's maximum grade value, this can be ignored. The UI is just confirming 
			with the user that this was their intention. However, if the grade item does not allow the mark to exceed the maximum grade value, it will appear as an error message and
			the user is forced to give a grade less than the maximum grade value.
		</p>
         <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/manual_upload_error.png">
        
        
        <h2>Report Page</h2>
        <p>The report page gives a summary of the user's upload. It shows how many grades were successfully set by the Brightspace API, any errors from the API, 
			and a summary of the students that had grades changed. 
		</p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/report_page_help.png">
		
        <h2>Logout</h2>
        <p>The user can logout (end their MLS session) by pressing the logout button of the navigation bar. </p>
        <img class="prototype-img" src="<?=$PATH_TO_STATIC?>/img/logout.png">
  
        <h3 id="toc_exclude">Version 1.0 - 11/14/2017</h3>
        <p>Author: Hind Althabi</p>
        <h3 id="toc_exclude">Version 2.0 - 11/29/2017</h3>
        <p>- Added more detail to the Introduction.</p>
        <p>- Added reference links.</p>
        <p>Author: Hind Althabi</p>
		<h3 id="toc_exclude">Version 3.0 - 12/05/2017</h3>
        <p>- Fixed spelling and grammar</p>
        <p>- Updated images to current UI.</p>
        <p>Author: Sarah Johnston</p>
        
    </body>
    <style>
        #file-structure {
            list-style: none;
        }
    
    img {
        width: 65%;
        margin: 20px 0px;
        
    }
    </style>
    
</html>

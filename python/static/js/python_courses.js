$(document).ready(getCourses);


/*
 * Ajax call to get list of courses
 */
function getCourses() 
{ 
    // Show loading 
	$('.loader-box').removeClass('hidden');
	
	$.ajax({
		type        : 'POST', 
		url         : '/get_courses', 
		dataType    : 'json',
		success     : showCourses
		});

}

/*
* Function to display returned courses
*/
function showCourses(courses)
{
   // Hide loader
	$('.loader-box').addClass('hidden'); 
}



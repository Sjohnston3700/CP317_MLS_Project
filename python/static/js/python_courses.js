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
		url         : '/actions/get_courses.py', 
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
	
	for (var i = courses.length-1; i >= 0; i--)
	{
	    var course = courses[i];
	    new_course = $('.templates .accordion').clone(true, true);
	    new_course.removeClass('accordion-template');
	    new_course.html(course.name);
	    new_course.removeClass('hidden');
	    new_course.addClass( course.id.toString() );
	    
	    
	    var grade_items = course.grade_items;
	    new_grade_items = $('.templates .panel').clone(true, true);
	    if (grade_items.length == 0)
	    {
	        new_grade_items.html('<p>No grade items for this course.</p>');
	    }
	    else
	    {
	        var new_html = '';
	        for (var ii=0;ii<grade_items.length; ii++)
	        {
	            var grade_item = grade_items[ii];
	            new_html = new_html + '<a class="grade-link" href="/index.py?page=upload&courseId=' + course.id + '&gradeItemId=' + grade_item.id + '">' + grade_item.name + '</a>'
	        }
	        new_grade_items.html( new_html );
	    }
	    new_grade_items.removeClass('hidden');
	    new_grade_items.removeClass('panel-template');
	    
	    
	    new_course.insertAfter('#available-courses');
	    new_grade_items.insertAfter( $( ".accordion."+course.id.toString() ) );
	    
	       
	
	}
	accordion();
}



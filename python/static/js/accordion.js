$(document).ready(function() {

$(document).on('click', '.course-item > a', function(e){
	e.preventDefault();
		var trigger = $(this);
		var course = trigger.parents('.course-item');
		var grades = course.find('.course-grades');

		if(course.hasClass('active')) {
			course.removeClass('active');
		} else {
			course.addClass('active');
		}
	});
});

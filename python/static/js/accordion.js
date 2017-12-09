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
    
$(document).ready(function() {
	var acc = $('.accordion');
	var i;

	for (i = 0; i < acc.length; i++) {
			acc[i].onclick = function() {
			this.classList.toggle('active');
			var panel = this.nextElementSibling;
			panel.classList.toggle('open');
			if (panel.style.maxHeight) {
				panel.style.maxHeight = null;
			} 
			else {
				var height = parseInt(panel.scrollHeight) + 30;
				panel.style.maxHeight = height + "px";
			}
		}
	}
}); 
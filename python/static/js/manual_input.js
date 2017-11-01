$('.remove-student').click(function() {
	var id = $(this).attr('id');
	id = id.slice(7);
	$('#student-' + id).remove();
});
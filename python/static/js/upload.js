$('#upload-target').on('load', function(){
		var result = $(this).contents().find('body').html();
		var grades = JSON.parse(result);
		sendToErrorChecking(grades);
});
	

function sendToErrorChecking(data) { 
	// Clear all previous forms and error messages
	$('.modal-body').html('');
	var formData = {
		grades: data
	}

	$.ajax({
		type        : 'POST', 
		url         : 'actions/error_checking.php', 
		data        : formData, 
		dataType    : 'json', 
		encode      : true,
		success     : function(data) {
						if (isNaN(data)) {
							for (var i = 0; i < data.length; i++) {
								var errorForm = $('#modal-form-template').clone();
								var formId = 'error-form-' + data[i].id;
								var error;
								var msg;

								errorForm.find('#name').text(data[i].name + ', ' + data[i].id);
								errorForm.attr('id', formId);
								errorForm.appendTo('.modal-body');
								errorForm.removeClass('hidden');
								errorForm.removeClass('modal-form-template');
								errorForm.find('#comment').text(data[i].comment);
								errorForm.find('#grade').val(data[i].value);

								if (data[i].type == 0) {
									error = $('.modal-warning-template').clone();
									error.removeClass('modal-warning-template');
									msg = '<strong>WARNING: </strong> ';
								} 
								else if (data[i].type == 1) {
									error = $('.modal-error-template').clone();
									error.removeClass('modal-error-template');
									msg = '<strong>ERROR: </strong> ';
								}

								error.html(msg + data[i].msg);
								error.removeClass('hidden');
								error.insertBefore(errorForm);
							}
						}
						showModalWithoutClose('error-message-modal');
					}
		});
}	

$('.remove-student').click(function() {
	var id = $(this).attr('id');
	id = id.slice(7);
	$('#student-' + id).remove();
});

$('#manual-upload').click(function() {
	var forms = $('.upload-form');
	var grades = [];
	for (var i = 0; i < forms.length; i++) {
		var grade = {};
		var formId = forms[i].id;
		var form = $('#' + formId);
		
		grade.id = formId.slice(8);
		grade.value = form.find('#grade').val();
		grade.comment = form.find('#comment').val();
		grade.name = form.find('#name').text();
		
		grades.push(grade);
	}
	sendToErrorChecking(grades)
});
var globalGrades = [];
$('#upload-target').on('load', function(){
		var result = $(this).contents().find('body').html();
		var grades = JSON.parse(result);
		sendToErrorChecking(grades);
});
	
function updateGlobalGrades(grades) {
	var index;
	var grade;
	for (var i = 0; i < globalGrades.length; i++) {
		index = findGrade(globalGrades[i].id, grades);
		if (index > -1) {
			grade = grades[index];
			globalGrades[i].id = grade.id;
			globalGrades[i].value = grade.value;
			globalGrades[i].comment = grade.comment;
			globalGrades[i].name = grade.name;
		} 
		else {
			globalGrades.splice(i, 1);
			i--;
		}
	}
}

function findGrade(id, grades) {
	for (var i = 0; i < grades.length; i++) {
		if (String(grades[i].id) == String(id)) {
			return i;
		}
	}
	return -1;
}

function sendToErrorChecking(data) { 
	// Clear all previous forms and error messages
	$('.error-form').remove();
	$('.modal-body').html('');
	
	//Set data to global variable in case user re-submits
	globalGrades = data;
	
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
								var errorForm = $('.templates .modal-form-template').clone();
								var formId = 'error-form-' + data[i].id;
								var error;
								var msg;
								
								errorForm.find('#name').text(data[i].name);
								errorForm.attr('id', formId);
								
								errorForm.addClass('error-form');
								errorForm.removeClass('hidden');
								errorForm.removeClass('modal-form-template');
								errorForm.find('#comment').text(data[i].comment);
								errorForm.find('#grade').val(data[i].value);
								errorForm.appendTo('.modal-body');

								if (data[i].type == 0) {
									error = $('.templates .modal-warning-template').clone();
									error.removeClass('modal-warning-template');
									msg = '<strong>WARNING: </strong> ';
								} 
								else if (data[i].type == 1) {
									error = $('.templates .modal-error-template').clone();
									error.removeClass('modal-error-template');
									msg = '<strong>ERROR: </strong> ';
								}

								error.html(msg + data[i].msg);
								error.removeClass('hidden');
								error.insertBefore(errorForm);
							}
							showModalWithoutClose('error-message-modal');
						}
						else {
							closeModal('error-message-modal');
							// Success, go to report page
						}
					} 
					
		});
}	

$('.remove-student').click(function() {
	var id = $(this).attr('id');
	id = id.slice(7);
	$('#student-' + id).remove();
});

$('#resubmit').click(function() {
	var forms = $('.modal-body .error-form');
	var grades = [];
	for (var i = 0; i < forms.length; i++) {
		var grade = {};
		var formId = forms[i].id;
		var id = formId.slice(11);
		var form = $('#' + formId);

		grade.id = id;
		grade.value = form.find('#grade').val();
		grade.comment = form.find('#comment').val();
		grade.name = form.find('#name').text();
		grades.push(grade);
	}
	updateGlobalGrades(grades);
	sendToErrorChecking(globalGrades);
});

$('#cancel-upload').click(function() {
	closeModal('error-message-modal');
});

$('#manual-upload').click(function() {
	var forms = $('.upload-form');
	var grades = [];
	for (var i = 0; i < forms.length; i++) {
		var grade = {};
		var formId = forms[i].id;
		var form = $('#' + formId);
		var id = formId.slice(8);
		
		grade.id = id;
		grade.value = form.find('#grade').val();
		grade.comment = form.find('#comment').val();
		grade.name = form.find('#name').text();

		grades.push(grade);
	}
	sendToErrorChecking(grades)
});
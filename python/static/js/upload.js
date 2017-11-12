/*
	 Automated upload and manual upload JS functions
	 Author: Sarah Johnston
	 Usage: Controller used with upload.html. Functions and listeners used 
			  to populate error checking modal, send JSON grade object to error_checking.php, 
			  and display error messages
 */

var globalGrades = [];

/**
 * Listener for iframe loading. Required to upload and parse file without 
 * page reloading. parse_file.php returns JSON object from parsed file 
 * and puts into iframe. This listener function gets the contents of the 
 * iframe and calls error checking function.
 */
$('#upload-target').on('load', function() {
		$('.upload-file-error').remove();
		var result = $(this).contents().find('body').html();
		var json = JSON.parse(result);
		
		if (json.length > 0 && json[0].hasOwnProperty('id')) {
			sendToErrorChecking(json);
		} 
		else {
			for (var i = 0; i < json.length; i++) {
				var error = $('.templates .modal-error-template').clone(true, true);
				error.removeClass('modal-error-template');
				error.removeClass('hidden');
				error.addClass('upload-file-error');
				if (json[i].hasOwnProperty('line')) {
					msg = '<strong>ERROR (line ' + json[i].line + '): </strong>' + json[i].msg;
				}
				else {
					msg = '<strong>ERROR: </strong>' + json[i].msg;
				}
				
				error.html(msg);
				error.insertBefore($('#file-error'));
			}
		}
		
});

/**
 * Updates the global grades array when user resubmits grades.
 * @param {Array} grades - New JSON object of grades from error checking modal
 */

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

/**
 * Finds grade with 'id' in array 'grades'
 * @param {Integer} id - Id of student to find
 * @param {Array} grades - Array of grade objects to check
 * @return {Integer} Index of found grade item with student id 'id'
 */
function findGrade(id, grades) {
	for (var i = 0; i < grades.length; i++) {
		if (String(grades[i].id) == String(id)) {
			return i;
		}
	}
	return -1;
}

/**
 * Ajax call to error_checking.php. On return, if no errors, redirects 
 * to report page. Otherwise, displays error modal with error messages 
 * returned from error_checking.php
 * @param {Array} data - array of JSON grade objects to send for error checking 
 */
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
						if (data.length > 0) {
							for (var i = 0; i < data.length; i++) {
								var errorForm = $('.templates .modal-form-template').clone(true, true);
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
								errorForm.find('.remove-student-error').attr('id', 'remove-' + data[i].id);

								if (data[i].type == 0) {
									error = $('.templates .modal-warning-template').clone(true, true);
									error.removeClass('modal-warning-template');
									msg = '<strong>WARNING: </strong> ';
								} 
								else if (data[i].type == 1) {
									error = $('.templates .modal-error-template').clone(true, true);
									error.removeClass('modal-error-template');
									msg = '<strong>ERROR: </strong> ';
								}
								error.addClass('error-msg-' + data[i].id);
								error.html(msg + data[i].msg);
								error.removeClass('hidden');
								error.insertBefore(errorForm);
							}
							showModalWithoutClose('error-message-modal');
						}
						else {
							closeModal('error-message-modal');
							// Success, go to report page
							window.location.href = 'index.php?page=report';
						}
					} 
					
		});
}	

/**
 * Listener for clicking remove student button (red x) on manual entry.
 */
$('.remove-student').click(function() {
	var id = $(this).attr('id');
	id = id.slice(7);
	$('#student-' + id).remove();
});

/**
 * Listener for clicking remove student button (red x) on error modal
 */
$('.remove-student-error').click(function() {
	var id = $(this).attr('id');
	id = id.slice(7);
	$('#error-form-' + id).remove();
	
	// Remove all error messages for that person
	$('.error-msg-' + id).remove();
});

/**
 * Click event for when user resubmits grades. Gets changes from modal 
 * then updates global grades array and sends to error checking again.
 */
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

/**
 * Closes button for error checking modal.
 */
$('#cancel-upload').click(function() {
	closeModal('error-message-modal');
});

/**
 * Submits manual upload form. Goes through student forms and 
 * makes array of JSON objects
 */
$('#manual-upload').click(function() {
	var forms = $('#manual-grade-input .upload-form');
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

/**
 * Listens for submitting of update max.
 */
$('#update-max').click(function() {
	var form = $('#update-max-form');
	var max = form.find('#max-grade').val();
	updateMax(max, 'update-max-error');
});

/**
 * Listens for submitting of update max on modal.
 */
$('#update-max-modal').click(function() {
	var form = $('#update-max-form-modal');
	var max = form.find('#max-grade-modal').val();
	updateMax(max, 'update-max-error-modal');
});


/**
 * Ajax call to update_max.php. On return, if no errors, shows 
 * success message. Otherwise, displays error modal with error messages 
 * returned from update_max.php
 * @param {String} max - grade max from input
 * @param {String} id - element id to put the error messages before
 */
function updateMax(max, id) { 
	// Clear all previous forms and error messages
	$('.update-max-error').remove();
	
	var formData = {
		max: max
	}

	$.ajax({
		type        : 'POST', 
		url         : 'actions/update_max.php', 
		data        : formData, 
		dataType    : 'json', 
		encode      : true,
		success     : function(data) {
						if (data.length > 0) {
							for (var i = 0; i < data.length; i++) {
								var error;
								var msg;

								error = $('.templates .modal-error-template').clone(true, true);
								error.removeClass('modal-error-template');
								error.removeClass('hidden');
								error.addClass('update-max-error');
								msg = '<strong>ERROR: </strong> ';
								error.html(msg + data[i].msg);
								
								error.insertBefore('#' + id);
							}
						}
						else {
								var success;
								var msg;

								success = $('.templates .modal-success-template').clone(true, true);
								msg = 'Grade maximum updated successfully';
								
								success.removeClass('hidden');
								success.removeClass('modal-success-template');
								success.addClass('update-max-error');
								success.html(msg);
								success.insertBefore('#' + id);
						}
					} 
					
		});
}	
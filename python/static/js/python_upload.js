/*
	 Automated upload and manual upload JS functions
	 Author: Sarah Johnston
     Modified by Harold Hodgins to work with python and flask
	 Usage: Controller used with upload.html. Functions and listeners used 
			  to populate error checking modal, send JSON grade object to error_checking, 
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
		var result = $(this).contents().find('body').html();
		
        //this listener is called on every page load/reload
        //if no file uploaded, then result = html of page, so parse fails
        //don't need to do anything if no file
        try {
            var json = JSON.parse(result);
        } catch(e) {
            return;
        }
        
        //remove any existing error msgs
        $('.upload-file-error').remove();
		
		if (json.length > 0 && json[0].hasOwnProperty('id')) {
			sendToErrorChecking(json);
		} 
		else {
			var error = $('.templates .modal-error-template').clone(true, true);
			error.removeClass('modal-error-template');
			error.removeClass('hidden');
			error.addClass('upload-file-error');

			//if whole file was bad, just need to display 1 error msg describing problem
			//line property only exists if only problem with some lines
			if (!json[0].hasOwnProperty('line')) {
				msg = '<strong>ERROR: </strong>' + json[0].msg;
				error.html(msg);
				error.insertBefore($('#file-error'));
				return;
			}

			//else, problem with just some lines
			//dislay msg saying required format first
			msg = '<strong>ERROR: </strong>' + 'Format must be brightspace_id, grade, student_name, comment';
			error.html(msg);
			error.insertBefore($('#file-error'));

			//display msgs for each bad line
			for (var i = 0; i < json.length; i++) {
				var error = $('.templates .modal-error-template').clone(true, true);
				error.removeClass('modal-error-template');
				error.removeClass('hidden');
				error.addClass('upload-file-error');
				msg = '<strong>ERROR (line ' + json[i].line + '): </strong>' + json[i].msg;
				
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

    for (var i = 0; i<grades.length;i++)
    {
        grade = grades[i];
        index = findGrade( grade.id, globalGrades );
        if (index > -1)
        {
            globalGrades[index].id      = grade.id;
            globalGrades[index].value   = grade.value;
            globalGrades[index].comment = grade.comment;
            globalGrades[index].name    = grade.name;
			if (grade.hasOwnProperty('is_warning')) {
				globalGrades[index].is_warning = grade.is_warning;
			} else {
				globalGrades[index].is_warning = false;
			}
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
	
	// Show loading 
	$('.loader-box').removeClass('hidden');
	
	// Hide update max form on modal and <hr> 
	$('#update-max-form-modal').addClass('hidden');
	$('.hr').addClass('hidden');
	
	// Remove previous error messages
	$('.error-msg').remove();
	
	// Set data to global variable in case user re-submits
	globalGrades = data;
    console.log('data being sent');
	
    var formData = {
		'grades': data,
		'gradeItemId': gradeItemId,
		'courseId': courseId
	}

    console.log(JSON.stringify(formData));
    
	$.ajax({
		type        : 'POST', 
		url         : '/actions/error_checking.py', 
		data        : JSON.stringify(formData), 
		dataType    : 'json', 
		encode      : true,
		success     : function(data) {
                        console.log('Something got returned!');
                        console.log(data);
						if (data.length > 0) {
							//tracks if this error appears
							$greater_than_max_err = false;
							
							if (data[0].hasOwnProperty('error')) {
								// Overall error, not just error with one student (ex. they didn't submit any grades)
								error = $('.templates .modal-error-template').clone(true, true);
								error.removeClass('modal-error-template');
								msg = '<strong>ERROR: </strong> ';
								error.html(msg + data[0].error);
								error.removeClass('hidden');
								error.addClass('error-msg');
								error.insertBefore('#grade-submit-error');
								
								// Hide loading
								$('.loader-box').addClass('hidden');
								
								return;
							}
							// Clear all previous forms and error messages
							$('#error-message-modal .error-form').remove();
							$('#error-message-modal .modal-body').html('');
							$('.update-max-error').remove();
							//need to clear val in the case that the user tried to update to a bad max before re-uploading
							//don't want them to see that bad value displayed as max in field
							$('#update-max-form-modal').find('#max-grade-modal').val('');

							if (data[0].type == 2) {
								//display msgs for each bad line
								for (var i = 0; i < data.length; i++) {
									var error = $('.templates .modal-error-template').clone(true, true);
									error.removeClass('modal-error-template');
									error.removeClass('hidden');
									error.addClass('upload-file-error');
									msg = '<strong>ERROR (line ' + data[i].line + '): </strong>' + data[i].msg;
									
									error.html(msg);
									error.insertBefore($('#file-error'));
								}

								// Hide loading
								$('.loader-box').addClass('hidden');

								return;
							}
						
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
								errorForm.find('#grade').addClass('grade-input-warning');
								errorForm.appendTo('#error-message-modal .modal-body');
								errorForm.find('.remove-student-error').attr('id', 'remove-' + data[i].id);

								if (data[i].type == 0) {
									
									error = $('.templates .modal-warning-template').clone(true, true);
									error.removeClass('modal-warning-template');
									errorForm.addClass('is-warning');
									msg = '<strong>WARNING: </strong> ';
								} 
								else if (data[i].type == 1) {
									error = $('.templates .modal-error-template').clone(true, true);
									error.removeClass('modal-error-template');
									errorForm.addClass('is-error');
									msg = '<strong>ERROR: </strong> ';

									//checks if word "max" is in error msg
									//if true, means error is grade > max (not allowed for this gradeitem, since error)
									//so set var that later says to show update max form on modal
									if  (data[i].msg.indexOf('max') !== -1) {
										$greater_than_max_err = true;
									}
								}
								error.addClass('error-msg-' + data[i].id);
								error.html(msg + data[i].msg);
								error.removeClass('hidden');
								error.insertBefore(errorForm);
							}
							
							//if a grade > max error was found when iterating through errors
							//then display update max form
							if ($greater_than_max_err){
								$('#update-max-form-modal').removeClass('hidden');
								$('.hr').removeClass('hidden');
							}
							showModalWithoutClose('error-message-modal');
							$('.modal').animate({ scrollTop: 0 }, 'slow');
						}
						else {
							closeModal('error-message-modal');
							// Success, go to report page
							window.location.href = '/index.py?page=report&courseId=' + courseId + '&gradeItemId=' + gradeItemId;
						}
				
						// Hide loading
						$('.loader-box').addClass('hidden');
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
	
	// Now remove them from globalGrades
	var index = findGrade(grade.id, globalGrades);
	globalGrades.splice(index,1);

	//if all students have been removed, close modal
	if (globalGrades.length == 0) {
		closeModal('error-message-modal');
	}	
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
		
		grade.is_warning = forms[i].classList.contains('is-warning');
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
 * Closes button for error checking modal.
 */
$('#cancel-confirm').click(function() {
	closeModal('confirm-max-grade');
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
	sendToErrorChecking(grades);
});

/**
 * Opens modal to confirm if user wants to change grade maximum
 */
$('.open-confirm-max-grade').click(function() {
	var isModal = parseInt($(this).attr('modal-form'));
	if (isModal) {
		$('#update-max').addClass('hidden');
		$('#update-max-modal').removeClass('hidden');
	}
	else {
		$('#update-max').removeClass('hidden');
		$('#update-max-modal').addClass('hidden');
	}
	showModal('confirm-max-grade');
});

/**
 * Listens for submitting of update max.
 */
$('#update-max').click(function() {
	closeModal('confirm-max-grade');
	var form = $('#update-max-form');
	var max = form.find('#max-grade').val();
	updateMax(max, 'update-max-error');
});

/**
 * Listens for submitting of update max on modal.
 */
$('#update-max-modal').click(function() {
	closeModal('confirm-max-grade');
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
function updateMax(new_max, id) { 
	
	// Show loading 
	$('.loader-box').removeClass('hidden');
	
	var formData = {
		'new_max': new_max,
		'gradeItemId': gradeItemId,
		'courseId': courseId
	}

	$.ajax({
		type        : 'POST', 
		url         : '/actions/update_max.py', 
		data        : formData, 
		dataType    : 'json', 
		encode      : true,
		success     : function(data) {
							
						// Clear all previous forms and error messages
						$('.update-max-error').remove();
						
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
						else if (parseInt(data) != NaN){
								
								var success;
								var msg;
							
								$('#out-of').text(data);
								$('#max-grade').attr('placeholder', data);
                                $('#max-grade-modal').attr('placeholder', data);
                                $('.grade-label').text('/' + data);
							
								success = $('.templates .modal-success-template').clone(true, true);
								msg = 'Grade maximum updated successfully';
								
								success.removeClass('hidden');
								success.removeClass('modal-success-template');
								success.addClass('update-max-error');
								success.html(msg);
								success.insertBefore('#' + id);
						}
			
						// Hide loader
						$('.loader-box').addClass('hidden');
					} 
					
		});
}	

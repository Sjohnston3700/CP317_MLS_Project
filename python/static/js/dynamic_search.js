function createForm(name, id) {
	// Remove error messages where form will go
	$('.error-msg').remove();
	var form = $('.templates .upload-form-template').clone(true, true);

	form.removeClass('upload-form-template');
	form.removeClass('hidden');
	form.find('#name').text(name);
	form.find('.remove-student').attr('id', 'remove-' + id);
	form.attr('id', 'student-' + id);
	$("#manual-grade-input").append(form);

	addSuccessMsg(name + ' added');
}

function addSuccessMsg(msg) {
	//remove previous msg, if exists
	$('.search-msg').remove();

	//define msg and insert above search bar
	success = $('.templates .modal-success-template').clone(true, true);
	success.removeClass('hidden');
	success.removeClass('modal-success-template');
	success.addClass('update-max-error');
	success.addClass('search-msg');
	success.html(msg);
	success.insertBefore('#members');
}

function addErrorMsg(msg) {
	//remove previous msg, if exists
	$('.search-msg').remove();
	//define msg and insert above search bar
	error = $('.templates .modal-error-template').clone(true, true);
	error.removeClass('modal-error-template');
	error.removeClass('hidden');
	//error.removeClass('modal-success');
	error.addClass('update-max-error');
	error.addClass('search-msg');
	error.html(msg);
	error.insertBefore('#members');
}

function formExists(id) {
	var forms = $('#manual-grade-input .upload-form');
	var grades = [];
	for (var i = 0; i < forms.length; i++) {
		if (forms[i].id.slice(8) == id) {
			return true;
		}
		return false;
	}
}

// switches search type from name to id if a number is entered and vice-versa
$("#members").keyup(function() {
	var value = $("members").value;

	if (/\d/g.test(value) && options.getValue == "name") {
		options.getValue = "org_id";
		options.template.fields.description = "name";
		$("#members").easyAutocomplete(options);
		$("#members").focus();
	}
	else if (/^[a-zA-Z]+$/.test(value) && options.getValue == "org_id") {
		options.getValue = "name";
		options.template.fields.description = "org_id";
		$("#members").easyAutocomplete(options);
		$("#members").focus();
	}
});

// adds all students when ticked, removes them when unticked
$("#members-cb").change(function() {
	var checked = $("#members-cb").is(":checked");

	if (checked) {
		for (var i in options.data) {
			var name = options.data[i].name;
			var id = options.data[i].id;
			if (!formExists(id)) createForm(name, id);
		}
		addSuccessMsg('All students added');
	}
	else {
		$("#manual-grade-input").empty();
		addErrorMsg('All students removed');
	}
});

// unticks Select All checkbox when a student is removed
$(".remove-student").click(function() {
	$("#members-cb").prop("checked", false);
    addErrorMsg($(this).prev("div.inline").text() +' removed');
});

options = {
	data: members,
	getValue: "name",
	list:
		{
			match: {
				enabled: true
			},
			sort: {
				enabled: true
			},
			showAnimation: {
				type: "slide",
				time: 200,
				callback: function() {}
			},
			hideAnimation: {
				type: "fade",
				time: 200,
				callback: function() {}
			},
			onChooseEvent: function() {
				var name = $("#members").getSelectedItemData().name;
				var id = $("#members").getSelectedItemData().id;

				// Only make grade form if one doesn't exist for that student yet
				if (!formExists(id)) createForm(name, id);
				//display error msg that student already added
				else {
					addErrorMsg(name + ' already added');					
				}
			}
		},
	template: {
		type: "description",
		fields: {
			description: "org_id"
		}
	}
};

$("#members").easyAutocomplete(options);
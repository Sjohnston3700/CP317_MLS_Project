	function createForm(name,id) {
		// Remove error messages where form will go
		$('.error-msg').remove();
		var form = $('.templates .upload-form-template').clone(true, true);
		
		form.removeClass('upload-form-template');
		form.removeClass('hidden');
		form.find('#name').text(name);
		form.find('.remove-student').attr('id', 'remove-' + id);
		form.attr('id', 'student-' + id);
		
		$("#manual-grade-input").append(form);
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
	function handleInputKeyUp() {
		var value = document.getElementById("members").value;
		
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
	}

	// adds all students when ticked, removes them when unticked
	function handleCheckboxChange() {
		var checked = $("#members-cb").is(":checked");

		if (checked) {
			for (var i in options.data) {
				var name = options.data[i].name; 
				var id = options.data[i].id;
				if (!formExists(id)) createForm(name, id);
			}
		} 
		else {
			$("#manual-grade-input").empty();
		}
	}
	
	// unticks Select All checkbox when a student is removed
	$(".remove-student").click(function() {
		$("#members-cb").prop("checked", false);
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
			onClickEvent: function() {
				var name = $("#members").getSelectedItemData().name;
				var id = $("#members").getSelectedItemData().id;
				
				// Only make grade form if one doesn't exist for that student yet
				if (!formExists(id)) createForm(name,id);
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
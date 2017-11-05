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
		
	var options = {
		data: [],
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
				if (!formExists(id)) {
					
					var form = $('.templates .upload-form-template').clone(true, true);

					form.removeClass('upload-form-template');
					form.removeClass('hidden');
					form.find('#name').text(name);
					form.find('.remove-student').attr('id', 'remove-' + id);
					form.attr('id', 'student-' + id);

					$("#manual-grade-input").append(form);
				}
			}
		},
		template: {
			type: "description",
			fields: {
				description: "id"
			}
		}
	};
//
//	{% for member in course.get_members() %}
//		options.data.push({name:"{{member.get_name()}}", id:"{{member.get_org_id()}}"});
//	{% endfor %}
	
	options.data = [ 
		{ name: 'Sarah Johnston', id: '12345'},
		{ name: 'Johnston Doe', id: '34567'}
	];

	$("#members").easyAutocomplete(options);

	function switchSearchType() {
		var value = document.getElementById("members").value;
		if (/\d/g.test(value) && options.getValue == "name") {
			options.getValue = "id";
			options.template.fields.description = "name";
			$("#members").easyAutocomplete(options);
			$("#members").focus();
		} 
		else if (/^[a-zA-Z]+$/.test(value) && options.getValue == "id") {
			options.getValue = "name";
			options.template.fields.description = "id";
			$("#members").easyAutocomplete(options);
			$("#members").focus();
		}
	}
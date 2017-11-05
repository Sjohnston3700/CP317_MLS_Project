<h1>CS123 - Test Course - Lab Report 1</h1>
<h2>Out of: <strong>150</strong> marks</h2>
<hr>
<input type="text" class="input" placeholder="Grade item is now out of...">
<button class="btn btn-success">Update maximum</button>
<hr>
<h2>Automated Upload</h2>
<div class="page-section">
	<h2>Upload a File</h2>
	  <form id="upload-automated" action="actions/file_parse.php" method="POST" enctype="multipart/form-data" target="upload-target">
         	<input type="file" name="file" id="file">
          <p></p>
	  		<button class="btn" type="submit">Upload Grades File</button>
      </form>
	  <iframe class="hidden-iframe" id="upload-target" name="upload-target" src="#" style="width:0;height:0;border:0px solid #fff;"></iframe>   
</div>
<h2>Manual Grade Input</h2>
<div class="page-section">
	<h4>Search to add a student: </h4>
	<form>	
		<input id="members" class="input" type="text" onkeyup="switchSearchType()" placeholder="Enter Student Name or ID...">
		<div class="form-checkbox">
			<input type="checkbox">
			<label class="mini">Select all</label>
		</div>
	</form>
	<hr>
	<div id="manual-grade-input">
	<!-- foreach student
	<form class="upload-form" id="student-1">
		<h3><div id="name" class="inline">John Doe</div><button type="button" class="btn btn-error btn-remove inline remove-student" id="remove-1">x</button></h3>
		<div class="form-group">
			<label>Grade: </label>
			<input id="grade" name="grade" type="text" placeholder="Grade">
		</div>	
		<textarea id="comment" name="comment" class="input" placeholder="Student feedback..." resize="false"></textarea>
	</form>
	<form class="upload-form" id="student-2">
		<h3><div id="name" class="inline">Jane Doe</div><button type="button" class="btn btn-error btn-remove inline remove-student" id="remove-2">x</button></h3>
		<div class="form-group">
			<label>Grade: </label>
			<input id="grade" name="grade" type="text" placeholder="Grade">
		</div>	
		<textarea id="comment" name="comment" class="input" placeholder="Student feedback..." resize="false"></textarea>
	</form> -->
	</div>
	<button type="button" id="manual-upload" class="btn submit-btn">Upload grades to MLS</button>
</div>
<div id="error-message-modal" class="modal">
	<div class="modal-content">
		<div class="modal-header">
			<span class="close">&times;</span>
			<h2>Errors With Your Grade Upload</h2>
			<hr>
			<input type="text" class="input" placeholder="Grade item is now out of...">
			<button class="btn btn-success">Update maximum</button>
			<hr>
		</div>
		<div class="modal-body">
		</div>
		<div class="modal-footer">
			<button id="resubmit" class="btn btn-success">Re-Upload</button>
			<button id="cancel-upload" class="btn btn-error">Cancel Upload</button>
		</div>
	</div>
</div>
<!-- Template HTML -->
<div class="templates">
	<p class="modal-warning modal-warning-template hidden"></p>
	<p class="modal-error modal-error-template hidden"></p>
	<form class="modal-form-template form-wide hidden" id="modal-form-template">
		<h3><div id="name" class="inline"></div><button type="button" class="btn btn-error btn-remove inline remove-student-error">x</button></h3>
		<div class="form-group">
			<label>Grade: </label>
			<input type="text" name="grade" id="grade" placeholder="Enter grade">
		</div>	
		<textarea class="input" name="comment" id="comment" placeholder="Student feedback..." resize="false"></textarea>
	</form>
	<form class="upload-form upload-form-template hidden">
		<h3><div id="name" class="inline"></div><button type="button" class="btn btn-error btn-remove inline remove-student">x</button></h3>
		<div class="form-group">
			<label>Grade: </label>
			<input id="grade" name="grade" type="text" placeholder="Enter grade...">
		</div>	
		<textarea id="comment" name="comment" class="input" placeholder="Student feedback..." resize="false"></textarea>
	</form>
</div>
<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/upload.js"></script>
<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/jquery.easy-autocomplete.js"></script>
<script>
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

</script>
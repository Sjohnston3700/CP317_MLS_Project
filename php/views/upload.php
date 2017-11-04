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
		
		<input type="text" class="input" placeholder="Enter Student Name or ID...">
		<div class="form-checkbox">
			<input type="checkbox">
			<label class="mini">Select all</label>
		</div>
	</form>
	<hr>
	<!-- foreach student -->
	<form id="student-1">
		<h3>John Doe<button type="button" class="btn btn-error btn-remove inline remove-student" id="remove-1">x</button></h3>
		<div class="form-group">
			<label>Grade: </label>
			<input type="text" placeholder="Grade out of /100">
		</div>	
		<textarea class="input" placeholder="Student feedback..." resize="false"></textarea>
	</form>
	<form id="student-2">
		<h3>Jane Doe<button type="button" class="btn btn-error btn-remove inline remove-student" id="remove-2">x</button></h3>
		<div class="form-group">
			<label>Grade: </label>
			<input type="text" placeholder="Grade out of /100">
		</div>	
		<textarea class="input" placeholder="Student feedback..." resize="false"></textarea>
	</form>
	<button class="btn submit-btn">Upload grades to MLS</button>
</div>
<div id="change-total-modal" class="modal">
	<div class="modal-content">
		<div class="modal-header">
			<span class="close">&times;</span>
			<h3>Change grade item total</h3>
		</div>
		<div class="modal-body">
			<input type="text" class="input" placeholder="Grade item now out of...">
		</div>
		<div class="modal-footer">
			<button class="btn btn-success">Update total</button>
			<button class="btn btn-error">Cancel</button>
		</div>
	</div>
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
			<button class="btn btn-success">Re-Upload</button>
			<button class="btn btn-error">Cancel Upload</button>
		</div>
	</div>
</div>
<!-- Template HTML -->
<p class="modal-warning modal-warning-template hidden"></p>
<p class="modal-error modal-error-template hidden"></p>
<form class="form-wide hidden" id="modal-form-template">
	<h3><div id="name" class="inline"></div><button class="btn btn-error btn-remove inline">x</button></h3>
	<div class="form-group">
		<label>Grade: </label>
		<input type="text" name="grade" id="grade" placeholder="Enter grade">
	</div>	
	<textarea class="input" name="comment" id="comment" placeholder="Student feedback..." resize="false"></textarea>
</form>
<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/manual_input.js"></script>
<script>
	
	$('#upload-target').on('load', function(){
		var result = $(this).contents().find('body').html();
		var grades = JSON.parse(result);
		sendToErrorChecking(grades);
	});
	
	
	function sendToErrorChecking(data) {   
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
								console.log(data)
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
	
</script>
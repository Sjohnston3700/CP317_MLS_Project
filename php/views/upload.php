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

<form class="form-wide hidden" id="modal-form-template">
	<p class="modal-warning"><strong>WARNING: </strong>Grade greater than the <strong>maximum grade value</strong></p>
	<h3>John Doe, 1234567<button class="btn btn-error btn-remove inline">x</button></h3>
	<div class="form-group">
		<label>Grade: </label>
		<input type="text" placeholder="Grade out of /100" value="70">
	</div>	
	<textarea class="input" placeholder="Student feedback..." resize="false">Good job on A1!</textarea>
</form>

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
		
			<form class="form-wide">
				<p class="modal-error"><strong>ERROR: </strong>Missing grade entry</strong></p>
				<h3>Jane Doe, 1234565<button class="btn btn-error btn-remove inline">x</button></h3>
				<div class="form-group">
					<label>Grade: </label>
					<input type="text" placeholder="Grade out of /100">
				</div>	
				<textarea class="input" placeholder="Student feedback..." resize="false">You need to put more effort in!</textarea>
			</form>
		</div>
		<div class="modal-footer">
			<button class="btn btn-success">Re-Upload</button>
			<button class="btn btn-error">Cancel Upload</button>
		</div>
	</div>
</div>
<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/manual_input.js"></script>
<script>
	
	$('#upload-target').on('load', function(){
		var result = $(this).contents().find('body').html();
		var grades = JSON.parse(result);
		sendToErrorChecking(grades);
	});
	
	
	function sendToErrorChecking(data) {   
		console.log('here');
//		$(".hide-warning").remove();
//		var fields = ['first', 'last', 'email','password', 'company', 'timezone', 'dept'];
//		for (i = 0; i < fields.length; i ++)
//		{
//			$("#" + fields[i]).css({"border-color": "rgb(223, 232, 241)", "border-width": "1px"});
//		}
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
							console.log(data);
							showModalWithoutClose('error-message-modal');
							var errorForm = $('#modal-form-template');
						}
			});
	}	
	
</script>
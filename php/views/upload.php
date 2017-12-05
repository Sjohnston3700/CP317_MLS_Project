<?php
	if (isset($_GET['grade_item']) && isset($_GET['course'])) 
	{
		$course = $user->get_course($_GET['course']);
		
		if ($course == null)
		{
			header('Location: index.php?page=courses');
			die();
		}
		
		$grade_item = $course->get_grade_item($_GET['grade_item']);
		
		if ($grade_item == null)
		{
			header('Location: index.php?page=courses');
			die();
		}
	}
	else 
	{
		header('Location: index.php?page=courses');
		die();
	}
?>
<div class="loader-box hidden">
	<div class="loader-msg">Talking to Brightspace API</div>
	<div class="loader"></div> 
</div>

<h1><strong><?=$course->get_name()?></strong> , <?=$grade_item->get_name()?></h1>
<h2>Out of: <strong id="out-of"><?=$grade_item->get_max()?></strong> marks</h2>
<hr>
<h2>Change Grade Maximum</h2>
<div class="page-section">
	<form class="form-wide" id="update-max-form">
		<div id="update-max-error"></div>
		<input type="number" class="input" id="max-grade" min="0" placeholder="<?=$grade_item->get_max()?>">
		<button type="button" modal-form="0" class="btn open-confirm-max-grade">Update grade maximum</button>
	</form>
</div>
<h2>Automated Upload</h2>
<div class="page-section">
	<div id="file-error"></div>
	  <form id="upload-automated" action="actions/file_parse.php" method="POST" enctype="multipart/form-data" target="upload-target">
         	<label id="file" class="custom-file-upload-btn">
				<i class="fa fa-cloud-upload"></i> Upload File
			</label>
			<input id="file" type="file" name="file"/>
          	<p></p>
	  		<button class="btn" type="submit">Upload Grades File</button>
      </form>
	  <iframe class="hidden-iframe" id="upload-target" name="upload-target" src="#" style="width:0;height:0;border:0px solid #fff;"></iframe>   
</div>
<h2>Manual Grade Input</h2>
<div class="page-section">
	<h4>Search to add a student: </h4>
	<form>	
		<input id="members" class="input" type="text" onkeyup="handleInputKeyUp()" placeholder="Enter Student Name or ID...">
		<div class="form-checkbox">
			<input id="members-cb" type="checkbox" onchange="handleCheckboxChange()">
			<label class="mini">Select all</label>
		</div>
	</form>
	<hr>
	<div id="manual-grade-input"></div>
	<div id="grade-submit-error"></div>
	<button type="button" id="manual-upload" class="btn submit-btn">Upload grades to MLS</button>
</div>
<div id="error-message-modal" class="modal">
	<div class="modal-content">
		<div class="modal-header">
			<span class="close">&times;</span>
			<h2>Errors With Your Grade Upload</h2>
			<hr class="hr">
			<form class="form-wide" id="update-max-form-modal">
				<div id="update-max-error-modal"></div>
				<input type="number" class="input" id="max-grade-modal" min="0" placeholder="<?=$grade_item->get_max()?>">
				<button type="button" modal-form="1" class="btn open-confirm-max-grade">Update grade maximum</button>
			</form>
			<hr class="hr">
		</div>
		<div class="modal-body">
		</div>
		<div class="modal-footer">
			<button id="resubmit" class="btn btn-success">Re-Upload</button>
			<button id="cancel-upload" class="btn btn-error">Cancel Upload</button>
		</div>
	</div>
</div>
<div id="confirm-max-grade" class="modal">
	<div class="modal-content">
		<div class="modal-header">
			<span class="close">&times;</span>
			<h2>Confirm</h2>
		</div>
		<div class="modal-body">	
			Are you sure you want to update grade maximum?
		</div>
		<div class="modal-footer">
			<button type="button" id="update-max-modal" class="btn btn-success">Confirm</button>
			<button type="button" id="update-max" class="btn btn-success">Confirm</button>
			<button id="cancel-confirm" class="btn btn-error">Cancel</button>
		</div>
	</div>
</div>
<!-- Template HTML -->
<div class="templates">
	<p class="modal-success modal-success-template hidden"></p>
	<p class="modal-warning modal-warning-template hidden"></p>
	<p class="modal-error modal-error-template hidden"></p>
	<form class="modal-form-template form-wide hidden" id="modal-form-template">
		<h3><div id="name" class="inline"></div><button type="button" class="btn btn-error btn-remove inline remove-student-error">x</button></h3>
		<div class="form-group">
			<input class="grade-input" type="text" name="grade" id="grade" placeholder="Enter grade">
			<p class="grade-label"></p>
		</div>	
		<textarea class="input" name="comment" id="comment" placeholder="Student feedback..." resize="false"></textarea>
	</form>
	<form class="upload-form upload-form-template form-med-wide hidden">
		<h3><div id="name" class="inline"></div><button type="button" class="btn btn-error btn-remove inline remove-student">x</button></h3>
		<div class="form-group">
			
			<input class="grade-input" id="grade" name="grade" type="text" placeholder="Enter grade...">
			<p class="grade-label"></p>
		</div>	
		<textarea id="comment" name="comment" class="input" placeholder="Student feedback..." resize="false"></textarea>
	</form>
</div>
<script>
	// Members for dynamic search
	var course = <?=$_GET['course']?>;
	var grade_item = <?=$_GET['grade_item']?>;
	var members = [ 
		<?php 
		foreach ($course->get_members() as $m) { 
			if ($m->get_role() == 101) {
				echo("{name: '" . $m->get_name() . "', id: '" . $m->get_id() . "', org_id: '" . $m->get_org_id() . "'},");
			}
		} 
		
		?>
	];
	
	// Set value of grade labels (ex /150)
	$('.grade-label').text('/<?=$grade_item->get_max()?>');

</script>
<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/upload.js"></script>
<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/jquery.easy-autocomplete.js"></script>
<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/dynamic_search.js"></script>
<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/upload_button.js"></script>
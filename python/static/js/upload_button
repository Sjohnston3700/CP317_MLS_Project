$(function(){

  var fileInput = $(':file')

  // When your file input changes, update the text for your button
  fileInput.change(function(){
	$this = $(this);
	// If the selection is empty, reset it
	if($this.val().length == 0) {
	  $('#file').text('Upload File');
	}else{
	  $('#file').text($this.val().replace("C:\\fakepath\\", ""));
	}
  })
  // When your fake button is clicked, simulate a click of the file button
  $('#file').click(function(){
	fileInput.click();
  }).show();
});
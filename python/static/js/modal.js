function displayModal(modalId, btnId) {
	
	var modal = $('#' + modalId);
	var btn = $('#' + btnId);
	
	btn.click(function() {
  		modal.css('display', 'block');
	});

	$('.close').click(function() {
		modal.css('display', 'none');
	});

	$(window).click(function(event) {
		if (event.target.id == modalId) {
			modal.css('display', 'none');
		}
	});
}


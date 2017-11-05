function showModalOnBtnClick(modalId, btnId) {
	
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

function showModalWithoutClose(modalId) {
	// Show modal
	var modal = $('#' + modalId);
	modal.css('display', 'block');
	
	// Close only if close button is clicked
	$('.close').click(function() {
		modal.css('display', 'none');
	});
}

function closeModal(modalId) {
	var modal = $('#' + modalId);
	modal.css('display', 'none');
}


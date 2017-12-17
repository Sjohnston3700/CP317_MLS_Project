// Close only if close button is clicked
function showModalWithoutClose(modalId) {
	var modal = $('#' + modalId);
	modal.css('display', 'block');
}

function closeModal(modalId) {
	var modal = $('#' + modalId);
	modal.css('display', 'none');
	//de-register listeners that may have been added
	//no need to check key and click input when modal not active
	$(window).off('keydown');
	$(window).off('click');
}

function showModal(modalId) {
	var modal = $('#' + modalId);
	modal.css('display', 'block');

	//check which update max button is being used
	if (!$('#update-max').hasClass('hidden')) {
		$('#update-max').focus();
	}
	else {
		$('#update-max-modal').focus();
	}

	$(window).keydown(function(e) {
		//focus cancel (right button) on right arrow press
		if (e.keyCode == 39) {
			e.preventDefault();
			$('#cancel-confirm').focus();
		}
		//focus confirm (left button) on left arrow press
		else if (e.keyCode == 37) {
			e.preventDefault();
			//check which update max button is being used
			if (!$('#update-max').hasClass('hidden')) {
				$('#update-max').focus();
			}
			else {
				$('#update-max-modal').focus();
			}
			
		}
		//close modal on ESC press
		else if (e.keyCode == 27) {
			e.preventDefault();
			closeModal(modalId);
		}
	});

	//close if click outside modal
	$(window).click(function(event) {
		if (event.target.id == modalId) {
			closeModal(modalId);
		}
	});
}

// Close if close X button is clicked
$('.close').click(function(e) {
	closeModal($(this).closest('.modal')[0].id);
});


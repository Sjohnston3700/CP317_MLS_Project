<div class="center">
	<h1 class="page-title">Welcome to ezMarker!</h1>
	<div class="btn-row">
		<a class="btn btn-xl" href="index.php?page=docs">Docs</a>
		<?php if ($authenticated) { ?>
			<a class="btn btn-xl" href="index.php?page=courses">Courses</a>
		<?php } 
		else { ?>
			<a class="btn btn-xl" href="index.php?page=courses">Login</a>
		<?php } ?>
	</div>
</div>
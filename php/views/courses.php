<?php 

$courses = $user->get_courses();

?>

<h2>Select a Grade Item</h2>
<?php foreach ($courses as $c) { ?>
	<button class="accordion"><?=$c->name?></button>
	<div class="panel">
		<?php if (sizeof($c->get_grade_items()) > 0) { ?>
			<?php foreach ($c->get_grade_items() as $g) { ?>
			<a class="grade-link" href="#"><?=$g->get_name()?></a>
			<?php } ?>
		<?php } else { ?>
			<p> No grade items for this course</p>
		<?php } ?>
	</div>
<?php } ?>


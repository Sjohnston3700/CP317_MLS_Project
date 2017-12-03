<?php 

$courses = $user->get_courses();

?>

<?php if (empty($courses)) { ?>
	<p>You do not have permission to set grades for any courses</p>
	<?php exit; ?>
<?php } ?>


<h2>Select a Grade Item</h2>
<?php foreach ($courses as $c) { ?>
	<div class="course-item">
		<a href = "#"><?=$c->get_name()?></a>
		<div class = "course-carat">▿</div>
		<div class = "course-grades" style = "display: none;">
			<?php if (sizeof($c->get_grade_items()) > 0) { ?>
				<?php foreach ($c->get_grade_items() as $g) { ?>
				<a class="grade-link" href="index.php?page=upload&course=<?=$c->get_id()?>&grade_item=<?=$g->get_id();?>"><?=$g->get_name()?></a>
				<?php } ?>
			<?php } else { ?>
				<p> No grade items for this course</p>
			<?php } ?>
		</div>
	</div>
<?php } ?>
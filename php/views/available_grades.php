<?php 

$courses = 
[
	{ 
		name: "Test Course",
		grade_items: 
			[
				{ name: 'A1'},
				{ name: 'A2'},
			] 
	},
	{ 
		name: "Test Course 2",
		grade_items: 
			[
				{ name: 'A1'},
				{ name: 'A2'},
			] 
	}
]
	
?>

<h2>Select a Grade Item</h2>
<?php foreach ($courses as $c) { ?>
	<button class="accordion">{{course.name}}</button>
	<div class="panel">
		<?php foreach ($courses.grade_items as $p) { ?>
		<a class="grade-link" href="#">{{ gradeItem.name }}</a>
		<?php } ?>
	</div>
<?php } ?>


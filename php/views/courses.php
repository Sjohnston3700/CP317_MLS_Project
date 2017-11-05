<?php 

$grade_items = array('A1', 'A2');

  $c1 = (object) [
    'name' => 'Test Course 1',
    'grade_items' => $grade_items,
  ];

  $c2 = (object) [
    'name' => 'Test Course 2',
    'grade_items' => $grade_items,
  ];

$courses = array($c1, $c2);
	
?>

<h2>Select a Grade Item</h2>
<?php foreach ($courses as $c) { ?>
	<button class="accordion"><?=$c->name?></button>
	<div class="panel">
		<?php foreach ($c->grade_items as $g) { ?>
		<a class="grade-link" href="#"><?=$g?></a>
		<?php } ?>
	</div>
<?php } ?>


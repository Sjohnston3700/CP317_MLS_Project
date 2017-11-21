<?php 

$course = $_GET['course'];
$grade_item = $_GET['grade_item'];

$grades = get_grade_values($course, $grade_item);

?>
<div class="page-section">
	<h1>Upload Complete</h1>
	<h3>5 of 10 grades uploaded successfully</h3>
	<hr>
	<table>
		<tr>
			<th>Name</th>
			<th>Grade</th>
		</tr>
		<?php foreach ($grades as $g) { ?>
		<tr>
			<td><?=$g['User']['DisplayName']?></td>
			<td><?=$g['GradeValue']['DisplayedGrade']?> ( <?=$g['GradeValue']['PointsNumerator'] . '/' . $g['GradeValue']['PointsDenominator'] ?> )</td>
		</tr>
		<?php } ?>
	</table> 
</div>


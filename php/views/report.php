<?php 

if (!isset($_SESSION['report']) || !isset($_GET['course']) || !isset($_GET['grade_item']))
{
	header('Location: index.php?page=courses');
}

$course = $_GET['course'];

if ($course == null)
{
	header('Location: index.php?page=courses');
}

$grade_item = $_GET['grade_item'];

if ($grade_item == null)
{
	header('Location: index.php?page=courses');
}

$grades = get_grade_values($course, $grade_item);
$success = $_SESSION['report']['successful'];
$total = $_SESSION['report']['total'];
$ids = $_SESSION['report']['successful_ids'];
?>
<div class="page-section">
	<h1>Upload Complete</h1>
	<h3><?=$success?> of <?=$total?> grades uploaded successfully</h3>
	<hr>
	<table>
		<tr>
			<th>Name</th>
			<th>Grade</th>
		</tr>
		<?php foreach ($grades as $g) { ?>
			<?php if (in_array($g['User']['Identifier'], $ids)) { ?>
		<tr>
			<td><?=$g['User']['DisplayName']?></td>
			<td><?=$g['GradeValue']['DisplayedGrade']?> ( <?=$g['GradeValue']['PointsNumerator'] . '/' . $g['GradeValue']['PointsDenominator'] ?> )</td>
		</tr>
			<?php } ?>
		<?php } ?>
	</table> 
</div>


<?php 

if (!isset($_SESSION['report']) || !isset($_GET['course']) || !isset($_GET['grade_item']))
{
	header('Location: index.php?page=courses');
	die();
}


$course = $user->get_course($_GET['course']);

if ($course == null)
{
	header('Location: index.php?page=courses');
	die();
}

$grade_item = $course->get_grade_item($_GET['grade_item']);

if ($grade_item == null)
{
	header('Location: index.php?page=courses');
	die();
}


if (isset($_SESSION['report']['errors']))
{
	$errors = $_SESSION['report']['errors'];
}
else 
{
	$grades = get_grade_values($_GET['course'], $_GET['grade_item']);
	$success = $_SESSION['report']['successful'];
	$total = $_SESSION['report']['total'];
	$ids = $_SESSION['report']['successful_ids'];
}

?>
<div class="page-section">
	<h1>Upload Complete for <?=$course->get_name()?>, <?=$grade_item->get_name()?></h1>
	<h3><?=$success?> of <?=$total?> grades uploaded successfully</h3>
	<?php if (isset($errors)) { ?>
		<?php foreach ($errors as $e) { ?>
			<p><?=$e['msg']?></p>
		<?php } ?>
	<?php } ?>
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


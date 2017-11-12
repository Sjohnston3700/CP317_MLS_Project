<?php
    require_once 'config.php';
	require_once $config['libpath'] . '/D2LAppContextFactory.php';

	ob_start();
    session_start();


	$PATH_TO_STATIC = '../../python/static';
	$PATH_TO_DOCS = '../../python/templates/';

    $page = isset($_REQUEST['page']) ? $_REQUEST['page'] : 'courses';

	/******************************* D2L Code Goes Here *********************************/
	//Skip this part if we already have a valid user context
//	if ((!isset($_SESSION['user_context']) || strlen($_SESSION['user_context']->getUserId()) > 0) && $page != 'token') {
//		$_SESSION['app_context'] = new D2LAppContext($config['appId'], $config['appKey']);
//
//		$app_url = 'http://localhost/CP317_MLS_Project/php/root/index.php?page=token';
//		//$app_url = "{$config['scheme']}://{$config['host']}:{$config['port']}{$config['route']}";
//		
//		// Get URL for authentication; this takes a callback address
//		$url = $_SESSION['app_context']->createUrlForAuthentication($config['lms_host'], $config['lms_port'], $app_url);
//		session_write_close();
//		// Redirect to D2L authentication page; user will be redirected back here after
//		header('Location: ' . $url);
//		die();
//	}

	/****************************************************************************************************/


    switch ($page)
    {
		case 'report':
            $contents = '../views/report.php';
            break;
		case 'courses':
            $contents = '../views/courses.php';
            break;
        case 'upload':
            $contents = '../views/upload.php';
            break;
 		case 'spmp':
 			$contents = $PATH_TO_DOCS . 'spmp.html';
 			break;
 		case 'requirements':
 			$contents = $PATH_TO_DOCS . 'requirements.html';
 			break;
 		case 'requirements_wrapper':
 			$contents = $PATH_TO_DOCS . 'requirements_wrapper.html';
 			break;
 		case 'analysis':
 			$contents = $PATH_TO_DOCS . 'analysis.html';
 			break;
 		case 'analysis_wrapper':
 			$contents = $PATH_TO_DOCS . 'analysis_wrapper.html';
 			break;
 		case 'design':
 			$contents = $PATH_TO_DOCS . 'design.html';
 			break;
 		case 'design_wrapper':
 			$contents = $PATH_TO_DOCS . 'design_wrapper.html';
 			break;
		default:
            $contents = '../views/courses.php';
            break;
    }

?>

<!DOCTYPE html>
<html lang="en">
	<head>
		<title>ezMarker</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0, minimal-ui">
		<link rel="shortcut icon" type="image/png" href="<?=$PATH_TO_STATIC?>/img/logo.png"/>
		<!-- JQuery -->
		<script src="<?=$PATH_TO_STATIC?>/js/jquery-3.2.1.min.js"></script>

		<!-- Stylesheets -->
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/main.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/nav.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/page_content.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/typography.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/forms.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/elements.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/home.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/docs.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/tables.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/upload_button.css">
		<link rel="stylesheet" href="<?=$PATH_TO_STATIC?>/css/easy_autocomplete.css">

		<!-- Fonts -->
		<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
		<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css">

	</head>
	<body>
		<ul class="horiz-nav">
			<img id="logo" src="<?=$PATH_TO_STATIC?>/img/logo.png">
			<li class="brand">
				<a href="/">
					ezMarker
				</a>
			</li>
			<li class="item"><a href="/courses">Courses</a></li>
			<li class="item"><a href="#">Help</a></li>
			<li class="name-section">
			    <span>Welcome, David Brown</span>
				<button onclick="window.location.href='/logout'" class="btn">Logout</button>
			</li>
		</ul>
		<div class="page-content-horiz">
			<?php require_once($contents); ?>
		</div>
	</body>

	<!-- JS Files -->
	<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/accordion.js"></script>
	<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/modal.js"></script>
</html>

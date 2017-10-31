<?php
    require_once "config.php";
	require_once $config['libpath'] . '/D2LAppContextFactory.php';
	
	ob_start();
    session_start();

	/******************************* All of the D2L code should go here *********************************/
	// Skip this part if we already have a valid user context
	if(!isset($_SESSION['user_context']) || strlen($_SESSION['user_context']->getUserId()) > 0) {
		$_SESSION['app_context'] = new D2LAppContext($config['appId'], $config['appKey']);
	
		// TODO: This gives error "invalid x_target", HOWEVER it seems that the user is authenticated when revisiting the page
		$app_url = "${config['scheme']}://${config['host']}:${config['port']}${config['route']}"; // $_SERVER['REQUEST_URI']

		// Get URL for authentication; this takes a callback address
		$url = $_SESSION['app_context']->createUrlForAuthentication($config['lms_host'], $config['lms_port'], $app_url);

		// Redirect to D2L authentication page; user will be redirected back here after
		header('Location: ' . $url);
		die();
	}
	/****************************************************************************************************/

	$PATH_TO_STATIC = "../../python/static";
    $page = isset($_REQUEST['page']) ? $_REQUEST['page'] : "home";


    switch ($page)
    {
		case "uploaded":
            $contents = "../views/grades_upload.php";
            break;
        case "upload":
            $contents = "../views/upload.php";
            break;
        default:
            $contents = "../views/available_grades.php";
            break;
    }
	
?>

<!DOCTYPE html>
<html lang="en">
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0, minimal-ui">
		
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
		
		<!-- Fonts -->
		<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">

	</head>
	<body>
		<ul class="horiz-nav">
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


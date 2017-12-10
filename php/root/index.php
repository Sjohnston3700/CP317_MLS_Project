<?php
	require_once '../wrapper/obj/OrgMember.php';
	require_once '../wrapper/obj/API.php';
    require_once 'config.php';

	ob_start();
    session_start();

	$DEBUG = true;
	$PATH_TO_STATIC = '../../python/static';
	$PATH_TO_DOCS = '../../python/templates/';

    $page = isset($_REQUEST['page']) ? $_REQUEST['page'] : 'home';
	$login_required = array('token', 'courses', 'upload', 'report', 'logout');
	$authenticated = false;

	// Only check for credentials if on one of these pages. Docs, home, and help do not require login
	if (in_array($page, $login_required))
	{
		if ($page == 'token' && isset($_GET['x_a']) && isset($_GET['x_b']))
		{
			header('Location: token.php?x_a=' . $_GET['x_a'] . '&x_b=' . $_GET['x_b']);
			die();
		}

		if ($page == 'logout' && isset($_SESSION['userId']) && isset($_SESSION['userKey']))
		{
			unset($_SESSION['userId']);
			unset($_SESSION['userKey']);
			unset($_SESSION['userName']);
			header("location: https://" . $config['lms_host'] . "/d2l/logout");
			die();
		}

		if (!isset($_SESSION['userId']) || !isset($_SESSION['userKey']))
		{
			$redirectPage = 'http://localhost/CP317_MLS_Project/php/root/index.php?page=token';
			$authContextFactory = new D2LAppContextFactory();
			$authContext = $authContextFactory->createSecurityContext($config['appId'], $config['appKey']);
			$hostSpec = new D2LHostSpec($config['lms_host'], $config['lms_port'], $config['protocol']);
			$url = $authContext->createUrlForAuthenticationFromHostSpec($hostSpec, $redirectPage);
			header('Location:' . $url);
			die();
		}
		

		// TA: 102, Instructor: 103
		$roles = array(102, 103);
		$user = new User($roles);
		if ($user != null)
		{	
			$_SESSION['userName'] = $user->get_full_name();
		}
	}

	//assume authenticated if name set
	if (isset($_SESSION['userName'])) {
		$authenticated = true;
	}

    switch ($page)
    {
		case 'home':
            $contents = '../views/home.php';
            break;
		case 'docs':
            $contents = '../views/docs.php';
            break;
		case 'report':
            $contents = '../views/report.php';
            break;
		case 'courses':
            $contents = '../views/courses.php';
            break;
        case 'upload':
            $contents = '../views/upload.php';
            break;
		 case 'help':
            $contents = '../views/help.php';
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
			$contents = '../views/home.php';
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
			<a href="index.php?page=home"><img id="logo" src="<?=$PATH_TO_STATIC?>/img/logo.png" ></a>
			<li class="brand">
				<a href="index.php?page=home">
					ezMarker
				</a>
			</li>
			<?php if ($authenticated) { ?>
				<li class="item"><a href="index.php?page=courses">Courses</a></li>
			<?php } ?>
			<!--<li class="item"><a href="index.php?page=docs">Docs</a></li>-->
			<li class="item"><a href="index.php?page=help">Help</a></li>
			<?php if ($authenticated) { ?>
			<li class="name-section">
			    <span>Welcome, <?=$_SESSION['userName']?></span>
				<button onclick="window.location.href='index.php?page=logout'" class="btn">Logout</button>
			</li>
			<?php } ?>
		</ul>
		<div class="page-content-horiz">
			<?php require_once($contents); ?>
		</div>
	</body>

	<!-- JS Files -->
	<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/accordion.js"></script>
	<script type="text/javascript" src="<?=$PATH_TO_STATIC?>/js/modal.js"></script>
</html>

<?php
require_once 'auth.php';

session_start();

$role = getUserRole();

if ($role !== 'guest') {
    // Capture the output buffer to get any error messages
    ob_start();
    $error_message = ob_get_clean();
    
    if (!empty($error_message)) {
        echo $error_message . "<br>";
    }
    die('You are not authorized to access this page');
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guest Panel</title>
</head>
<body>
    <h1>Welcome to the Guest Panel</h1>
    <p>You are logged in as a guest. To access more features, please become an admin.</p>
    <a href="logout.php">Logout</a>
</body>
</html>
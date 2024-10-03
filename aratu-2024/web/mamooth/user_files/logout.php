<?php
require_once 'auth.php';

// Call the logout function
logout();

// Redirect to the login page
header("Location: login.php");
exit();
?>
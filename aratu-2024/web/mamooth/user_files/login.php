<?php
require_once 'auth.php';

session_start();
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];
    
    if (login($username, $password)) {
        // Successful login, refresh
        header("Location: login.php");
    } else {
        $error = "Invalid username or password";
    }
}
// Check if user is already authenticated
$role = getUserRole();
if ($role === 'admin') {
    header("Location: admin.php");
    exit();
} elseif ($role === 'guest') {
    header("Location: guest.php");
    exit();
}

// Check for auth error messages
if (isset($_SESSION['auth_error'])) {
    $error = $_SESSION['auth_error'];
    unset($_SESSION['auth_error']); // Clear the error message after displaying
}



?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Mamooth</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f0f0; }
        form { background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input { display: block; margin: 10px 0; padding: 5px; width: 200px; }
        button { background-color: #4CAF50; color: white; border: none; padding: 10px 20px; cursor: pointer; }
        .error { color: red; margin-bottom: 10px; }
    </style>
</head>
<body>
    <form method="POST">
        <h2>Mamooth Login</h2>
        <?php if (isset($error)) echo "<p class='error'>$error</p>"; ?>
        <input type="text" name="username" placeholder="Enter username" required>
        <input type="password" name="password" placeholder="Enter password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>
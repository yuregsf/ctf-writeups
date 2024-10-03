<?php
require_once 'auth.php';

session_start();

// Capture any output (including error messages) from getUserRole()
ob_start();
$role = getUserRole();
$error_message = ob_get_clean();

if ($role !== 'admin') {
    if (!empty($error_message)) {
        // Store the error message in a session variable
        $_SESSION['auth_error'] = $error_message;
    }
    header('Location: login.php');
    exit();
}

$file_contents = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['file_path'])) {
    $file_path = $_POST['file_path'];
        $file_contents = file_get_contents($file_path);

        // check if it contains the header "# DEBUG FILE"
        if ( ( strpos($file_contents, '# DEBUG FILE') === false ) ) {
            $error = 'Invalid file. File must contain the header "# DEBUG FILE". Refusing to include it.';
            // output contents
            $html = '<pre>' . htmlspecialchars($error) . '</pre>';
            $html = $html . '<pre>' . htmlspecialchars($file_contents) . '</pre>';
            

            die ($html);
        
        }

        // if it contains the header, include it
        
        include $file_path;

   
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 300px;
            padding: 5px;
        }
        input[type="submit"] {
            padding: 5px 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border: 1px solid #ddd;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Welcome to the Admin Panel</h1>
    <p>This is a secure area. Only authenticated admin users can access this page.</p>
    
    <h2>File Reader</h2>
    <form method="POST">
        <label for="file_path">Enter file path:</label>
        <input type="text" id="file_path" name="file_path" required>
        <input type="submit" value="Read File">
    </form>

    <?php if (!empty($error)): ?>
        <p class="error"><?php echo htmlspecialchars($error); ?></p>
    <?php elseif (!empty($file_contents)): ?>
        <h3>File Contents:</h3>
        <pre><?php echo htmlspecialchars($file_contents); ?></pre>
    <?php endif; ?>

    <a href="logout.php">Logout</a>
</body>
</html>
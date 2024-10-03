 <?php

$version = phpversion();
header("X-Powered-By: PHP/$version");

session_start();


if (!isset($_SESSION['user'])) {
    $_SESSION['user'] = strval(rand());
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $value = $_POST['value'];
    echo $_SESSION['user'] . "\n";

    if (isset($value) && is_numeric($value) && $value > 0) {
        try {
            echo $value . "\n";
            echo sprintf("INSERT INTO payloads (user_id, payload) VALUES (%s, %s)", $_SESSION['user'], $value);
        } catch (Exception $e) {
            die("Error: " . $e->getMessage());
        }
    } else {
        die("hmmmmmm nop, try again. value needs to be numeric and > 0");
    }
} else {
    highlight_file(__FILE__);
}
?>

<?php

define('AES_KEY', 'S2RxyWfJHd6d5Ju9'); // fake key for deploy
define('AES_IV', str_repeat("\0", 16)); // 16 null bytes

function encrypt($data) {
    return openssl_encrypt($data, 'AES-256-CBC', AES_KEY, OPENSSL_RAW_DATA, AES_IV);
}

function decrypt($data) {

    $decrypted = openssl_decrypt($data, 'AES-256-CBC', AES_KEY, OPENSSL_RAW_DATA, AES_IV);

    if ($decrypted === false) {
        $error = openssl_error_string();
        throw new Exception("Decryption failed: " . $error);
    }
    // get first {, ignore junk before it. and if first char is not {, 
    if (strpos($decrypted, '{') !== 0) {
        $decrypted = substr($decrypted, strpos($decrypted, '{'));
    }
    return $decrypted;
}


function isAuthenticated() {
    if (!isset($_COOKIE['auth'])) {
        return false;
    }
    try {
        $auth_cookie = base64_decode($_COOKIE['auth']);

        if ($auth_cookie === false) {
            return false;
        }

        $decrypted = decrypt($auth_cookie);
        
        $data = json_decode($decrypted, true);

        return $data['role'];
    } catch (Exception $e) {
        echo 'Error: ' . $e->getMessage();
        return false;
    }
}

function getUserRole() {
    return isAuthenticated();
}

function login($username, $password) {
    if ($username === 'admin' && $password === 'iKnfyodsVO0WL00Gkkkkkkkkkk') { // fake password for deploy
        $role = 'admin';
    } elseif ($username === 'guest' && $password === 'guest') {
        $role = 'guest';
    } else {
        return false;
    }

    $data = json_encode(['role' => $role]);
    printf('%s', $data);
    
    $encrypted = encrypt($data);
    printf('%s', $encrypted);
    setcookie('auth', base64_encode($encrypted), time() + 3600, '/', '', true, true);
    return true;
}

function logout() {
    setcookie('auth', '', time() - 3600, '/', '', true, true);
}

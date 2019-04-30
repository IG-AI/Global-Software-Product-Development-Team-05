<?php
session_start(); // Starting Session
$error = ''; // Variable To Store Error Message
if (isset($_POST['submit'])) {
    if (empty($_POST['email']) || empty($_POST['password'])) {
        $error = "Email or Password is invalid";
    }
    else{
        // Define $username and $password
        $email = $_POST['email'];
        $password = $_POST['password'];
        $password=md5($password);
        // mysqli_connect() function opens a new connection to the MySQL server.
        $conn = mysqli_connect("localhost", "root", "password", "global");
        // SQL query to fetch information of registerd users and finds user match.
        $query = "SELECT email, password from registered_users  where email=? AND password=? LIMIT 1";
        // To protect MySQL injection for Security purpose
        $stmt = $conn->prepare($query);
        $stmt->bind_param("ss", $email, $password);
        $stmt->execute();
        $stmt->bind_result($email, $password);
        $stmt->store_result();
        if($stmt->fetch()) {
            //fetching the contents of the row
            // Redirecting To Profile Page
            $_SESSION['login_user'] = $email; // Initializing Session
            header("location: profile.php");
        }
        else{
            echo "Wrong email and/or password.";
        }
    }
    mysqli_close($conn); // Closing Connection
}
?>
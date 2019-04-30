<?php
$password = $_POST['password'];
$password = md5($password);
$email = $_POST['email'];
$firstname = $_POST['firstname'];
$lastname = $_POST['lastname'];


if (!empty($password) || !empty($email)) {
    $host = "localhost";
    $dbUsername = "root";
    $dbPassword = "password";
    $dbname = "global";
    //create connection
    $conn = new mysqli($host, $dbUsername, $dbPassword, $dbname);
    if (mysqli_connect_error()) {
        die('Connect Error(' . mysqli_connect_errno() . ')' . mysqli_connect_error());
    } else {
        $SELECT = "SELECT email From global.registered_users Where email = ? Limit 1";


        $INSERT = "INSERT Into global.registered_users (email,firstname,lastname,password) values(?, ?,?,?)";

        //Prepare statement
        $stmt = $conn->prepare($SELECT);
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $stmt->bind_result($email);
        $stmt->store_result();
        $rnum = $stmt->num_rows;
        if ($rnum == 0) {
            $stmt->close();
            $stmt = $conn->prepare($INSERT);
            $stmt->bind_param("ssss", $email, $firstname, $lastname, $password);
            $stmt->execute();
            header("Location:../login/index.php");
        } else {
            echo "Someone already register using this email";
        }
        $stmt->close();
        $conn->close();
    }
} else {
    echo "All field are required";
    die();
}
?>
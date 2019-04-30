<?php
include('login.php'); // Includes Login Script
if(isset($_SESSION['login_user'])){
header("location: profile.php"); // Redirecting To Profile Page
}
?>
<!DOCTYPE html>
<html>
<link rel="stylesheet" type="text/css" href="../Login/signin.css">

<head>
  <title>Login</title>
</head>
<body>
 <div id="login">
  <h2>Sign In</h2>
  <form action="" method="post">
      <label for="uname"><b>Email</b></label>
      <input type="text" placeholder="Enter Email" name="email" required>

      <label for="psw"><b>Password</b></label>
      <input type="password" placeholder="Enter Password" name="password" required>

      <input name="submit" class="loginbtn" type="submit" value=" Login ">

      <span><?php echo $error; ?></span>
  </form>
 </div>
</body>
</html>
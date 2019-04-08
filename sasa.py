<?php
$u=isset($_GET['u'])? $_GET['u']:'';
$u=addslashes($u);
$sql = "select * from user where user='$u'";
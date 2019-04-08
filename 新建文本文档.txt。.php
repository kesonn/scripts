<?php

header('content-type:text/html;charset=utf-8');
if(! isset($_GET['img']))
    header('Refresh:0;url=./index.php?img=hello.gif');
$file = $_GET['img'];
echo '<title>file:'.$file.'</title>';
$file = preg_replace("/[^a-zA-Z0-9\.]+/","", $file);
$file = str_replace("test","_", $file);
$txt = base64_encode(file_get_contents($file));

echo "<img src='data:image/gif;base64,".$txt."'/>";

/*
 * Can you find the flag file?
 *
 */

?>
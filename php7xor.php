<?php
//flag = $_POST['FLAG'];
$slist = str_split("`~!@#$%^&*()_+|\'\":;?/.,><");
$slen = count($slist);
for ($x=0; $x<$slen; $x++) {
	for ($x=0; $x<$slen; $x++) {
		$flag = '_' ^ $slist[$x];
		if(in_array($flag,$slist)){
			print_r($flag.' ^ '.$slist[$x].'<br>');
		}

	}
}

?>
<?php
function create_password($pw_length =  10) {  
	$randpwd = "";
	for ($i = 0; $i < $pw_length; $i++)  {  
		$randpwd .= chr(mt_rand(33, 126));  
	}  
	return $randpwd;  
}  
$T = time();
while(1){
	echo '\r\n';
	mt_srand($T);
	print_r($T);echo '\r\n';
	$pwd = urlencode(create_password());
	$req = get("http://www.loudong.org:801/tasks/f3.php?pwd=$pwd");
	echo strlen($req);echo '\r\n';
	if(strpos($req,'Wrong!<!--')){
		$T-=1;
	}else{
		print_r($pwd);
		break;
	}
}


function get($url){
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_HEADER, 0);
$output = curl_exec($ch);
curl_close($ch);
return $output;
}

function post($url,$data){
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
$output = curl_exec($ch);
curl_close($ch);
return $output;
}
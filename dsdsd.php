<?php


class Request{
	function get(){
	}
	function post($host,$port=80,$uri,$data,$headers=null){
		$flag = 0;
		$params = '';
		$errno = '';
		$errstr = '';
		$result ='';
		foreach ($data as $key=>$value) {
			if ($flag!=0) {
				$params .= "&";
				$flag = 1;
			}
		$params.= $key."="; $params.= urlencode($value);
		$flag = 1;
		}
		$length = strlen($params);
		$fp = fsockopen($host,$port,$errno,$errstr,10) or exit($errstr."--->".$errno);
		$header  = "POST ".$uri." HTTP/1.1\r\n";
		$header .= "Host: ".$host."\r\n";
		$header .= "Content-Type: application/x-www-form-urlencoded\r\n";
		$header .= "Cookie: ".$cookies."\r\n";
		foreach ($headers as $key=>$value) {
			$header .= $key.": ".$value."\r\n";
		}
		$header .= "Content-Length: ".$length."\r\n";
		$header .= "Connection: keep-alive\r\n\r\n";
		$header .= $params."\r\n";
		fputs($fp,$header);
		$inheader = 1;
		while (!feof($fp)) {
			$line = fgets($fp,1024); //去除请求包的头只显示页面的返回数据
			if ($inheader && ($line == "\n" || $line == "\r\n")) {
				 $inheader = 0;
			}
			if ($inheader == 0) {
			  $result .= $line;
			}
		}
		fclose($fp);
		return $result;
	} 
}

?>
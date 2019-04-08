<?php
    include 'dbconnect.php';
    session_start();
    $data = json_decode(file_get_contents("php://input"));
    if (@$_REQUEST['op']) $op = $_REQUEST['op'];
    else $op = $data->op;

$debugfile = fopen("test_sysoption.txt","a");
fwrite($debugfile,"add by gbh: op = " . $op . "\n");	

    $empty = array();
    try {
        if ($op == 'getlicenseinfo') {
            $rows = $DB->SysOption->find(array('_id' => 'License'));
            if ($rows->hasNext()){
                foreach($rows as $r) {
                    $lic =$r['License'];
                }
                //$lic = "65794c6c72714c6d694c666c6b49336e703741694f694c6b754b336c6d37336c6d37336e765a486b7549726d746263694c434c6f72726a6c6a362f6f7234486c6a3763694f6949784d6a4d300a49697769357079413561536e3535536f356f693335705777496a6f694d7a41774969776935377530356f716b355969773570796635706532365a6530496a6f694d6a41784d5330774d5330770a4d534973497561596a7565376869493665794c6c704b6e6d744b55694f6949314d43497349756179732b574d6c794936496a45314d43497349756179732b574e6c794936496a45774d434a390a4c434a5465584e305a5730694f6e7369546e5674596d5679496a6f694d7a4177496977695257356b56476c745a534936496a49774d5445744d4445744d4445696658303d0a";
                $bytes = pack("H*",$lic);
                echo base64_decode($bytes);
            } else echo "{}";
        } else if ($op == 'setlicense') {
fwrite($debugfile,"add by gbh: setlicense new ...\n");		
            if ( !empty( $_FILES ) ) {
fwrite($debugfile,"add by gbh: _FILES is not empty ...\n");		

                $tempPath = $_FILES[ 'file' ][ 'tmp_name' ];
                $lic = file_get_contents($tempPath);
                $DB->SysOption->save(array('_id' => 'License','License' => $lic));
                $bytes = pack("H*",$lic);
                echo '"'.base64_decode($bytes).'"';
            } else {
fwrite($debugfile,"add by gbh: No files ...\n");		

                echo 'No files';
            }        
        } else if ($op == 'getMonitorInfo') {
            $rows = $DB->SysOption->find(array('_id' => 'Monitor'));
            foreach($rows as $r) {
                echo json_encode($r['keys']);
            }
        } else if ($op == 'getoption') {
            $rows = $DB->SysOption->find(array('_id' => 'Option'));
            foreach($rows as $r) {
                echo json_encode($r['Option']);
            }
        } else if ($op == 'getEventPara') {
            $rows = $DB->SysOption->find(array('_id' => 'EventPara'));
            foreach($rows as $r) {
fwrite($debugfile,"add by gbh: EventPara = " . $r['Values'] . "\n");	
                echo json_encode($r['Values']);
            }
        } else if ($op == 'getiniconfig') {
            $CONF = parse_ini_file("conf.ini",true);
            if (array_key_exists('HostName',$CONF['MongoDB'])) {
                $CONF['MongoDB']['HostIP'] = gethostbyname($CONF['MongoDB']['HostName']);
            }
            if (array_key_exists('HostName',$CONF['Redis'])) {
                $CONF['Redis']['HostIP'] = gethostbyname($CONF['Redis']['HostName']);
            }
            if (array_key_exists('HostName',$CONF['WebSocket'])) {
                $CONF['WebSocket']['HostIP'] = gethostbyname($CONF['WebSocket']['HostName']);
            }
            echo json_encode($CONF);
        } else if ($op == 'setoption') {
            $opt = $data->option;
            $DB->SysOption->save(array('_id' => 'Option','Option' => $opt));
            echo 'save ok';
        } else
            echo json_encode($empty);
    } catch (MongoException $e) {
        dbreturn(-2,'Error: ' . $e->getMessage());
    }   
fclose($debugfile);		
?>
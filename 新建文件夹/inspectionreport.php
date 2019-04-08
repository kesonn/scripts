<?php
    require_once('dbconnect.php');
    require_once('redisconnect.php');
    session_start();
    
    $data = json_decode(file_get_contents("php://input"));
    $op = $data->op;

//$debugfile = fopen("test_inspectionreport.txt","a");
//fwrite($debugfile,"op=" . $op ."\n");

    $empty = array();
    try {
        if ($op == 'query') {
            $inspections = $DB->InspectionReport->find()->sort(array('_id' => 1));
            if ($inspections->hasNext()){
               echo json_encode(iterator_to_array($inspections,false));
            }
        } else if ($op == 'save') {
            $nrecs = $data->item;
            $DB->InspectionReport->save($nrecs);
        } else if ($op == 'del') {
            $ids = $data->itemids;
            $DB->InspectionReport->remove(array('_id' => array( '$in' => $ids )));

        } else if ($op == 'getreportfilenames') {
            $file_names = Array();
            		
			$dir = "/opt/GreenLight_root/Report/";
//fwrite($debugfile,"dir=" . $dir ."\n");

			foreach (scandir($dir) as $filename){					
				if (stripos($filename,".xls")>0){
					$tmp_file['name'] = $filename;
					array_push($file_names,$tmp_file);
				}
			}	

			if (count($file_names)>0){
               echo json_encode($file_names);
            } else echo json_encode($empty);						

        } else if ($op == 'delfiles') {
            $filenames = $data->filenames;
			$dir = "/opt/GreenLight_root/Report/";

			foreach ($filenames as $filename){					
				$file = $dir . $filename;	
//fwrite($debugfile,"file=" . $file ."\n");
				unlink($file); 
			}	
			echo json_encode($empty);						

        } else if ($op == 'createreport') {
            $id = $data->id;
            $startTime = $data->starttime;
            $endTime = $data->endtime;
            
			$cmd_str = "Command=CreateReport,ReportID=$id,StartTime=$startTime,EndTime=$endTime,";
 //fwrite($debugfile,"cmd_str=" . $cmd_str ."\n");
            
			$ret = $redis->lpush("Inspection_Queue",$cmd_str);
            dbreturn($ret,"Redis lpush return.");
        } else echo json_encode($empty);
    } catch (MongoException $e) {
        dbreturn(-2,'Error: ' . $e->getMessage());
    }   
//fclose($debugfile);	
?>
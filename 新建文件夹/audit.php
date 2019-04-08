<?php
    include 'dbconnect.php';
    
    $data = json_decode(file_get_contents("php://input"));
    $op = $data->op;

    $empty = array();
    try {
        if ($op == 'query') {
            $audits = $DB->Audit->find()->sort(array('Time' => 1));
            if ($audits->hasNext()){
               echo json_encode(iterator_to_array($audits,false));
            }
        } else if ($op == 'save') {
            $nrec = $data->item;
            $DB->Audit->save($nrec);
        } else if ($op == 'getAuditsByUser') {
            $option = $data->option;
			$UserID = $option->UserID; 
            	
			if ($UserID == '#') {
				$qopt = array('Time' => array( '$gt' => ($option->d1), '$lt' => ($option->d2)));					
			}else {
				$qopt = array('UserID' => $UserID,'Time' => array( '$gt' => ($option->d1), '$lt' => ($option->d2)));
			}
			
			$qopt = array('Time' => array( '$gt' => ($option->d1), '$lt' => ($option->d2)));		
            //$rows = $DB->Audit->find($qopt);
			$rows = $DB->Audit->find($qopt)->sort(array('Time' => 1));
            if ($rows->hasNext()){
               echo json_encode(iterator_to_array($rows,false));
            } else echo json_encode($empty);            
        } else echo json_encode($empty);
    } catch (MongoException $e) {
        dbreturn(-2,'Error: ' . $e->getMessage());
    }    
?>
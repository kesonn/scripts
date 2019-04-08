<?php
    include 'dbconnect.php';
    session_start();
    $data = json_decode(file_get_contents('php://input'));
    $op = $data->op;

    $empty = array();
    try {
        if ($op == 'getcollectedfiles') {
            $objids = $data->objectids;
            $rows = $DB->CollectedFiles->find(array('ObjectID' => array('$in' => $objids )));
            if ($rows->hasNext()){
               echo json_encode(iterator_to_array($rows,false));
            } else echo '[]';       
        } else if ($op == 'getcollectedfile') {
            $fid = $data->fid;
            $rows = $DB->CollectedFiles->find(array('_id' => new MongoId($fid)));
            if ($rows->hasNext()){
               echo json_encode(iterator_to_array($rows,false));
            } else echo '[]';       
        } else if ($op == 'getgridfs') {
            $grid = $DB->getGridFS();
            $fsid = $data->fsid;
            $encode = $data->encode;
            $file = $grid->findOne(array('_id' => (new MongoId($fsid))));
            if ($file) {
                if (($encode=='no')||($encode=='utf8')) echo $file->getBytes();
                else echo iconv($encode,'utf-8',$file->getBytes());
            }
            else echo 'file not found!';
        } else if ($op == 'keepcollectfile') {
            $fid = new MongoId($data->fid);
            $keep = $data->keep;
            $newdata = array('$set' => array("Keep" => $keep));
            $DB->CollectedFiles->update(array('_id' => $fid ), $newdata);
            dbreturn(0,'OK');
        } else  echo json_encode($empty);
    } catch (MongoException $e) {
        dbreturn(-2,'Error: ' . $e->getMessage());
    }    
?>
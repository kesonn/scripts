<?php
    require_once('dbconnect.php');
    require_once('redisconnect.php');
    session_start();
    $data = json_decode(file_get_contents("php://input"));
    $op = $data->op;
    $empty = array();
//$file = fopen("test_execjob.txt","a");

	try {
        if ($op == 'query') {
            $rows = $DB->ExecJob->find();
            if ($rows->hasNext()){
               echo json_encode(iterator_to_array($rows,false));
            }
        } else if ($op == 'update') {
            $jid = $data->id;
            $jattrs = $data->attrs;
            
            $DB->ExecJob->update(
                array("_id" => new MongoId($jid)),
                array('$set' => $jattrs),
                array("upsert" => false)
            );
            dbreturn(0,"OK");
        }  else if ($op == 'getExecJob') {
            $id = $data->id;
            $rows = $DB->ExecJob->find(array('$or' => array(array('_id' => new MongoId($id)),array('ParentExecJobID' => $id)))
                                       ,array('Log' => false,'RunHistory' => false,'HostCommandList' => false));
            $recs = array();
            if ($rows->hasNext()){
               $recs = iterator_to_array($rows,false);
            }
            echo json_encode($recs);
        } else if ($op == 'getExecJobGroup') {
            $id = $data->id;
            $rows = iterator_to_array($DB->ExecJob->find(array('_id' => new MongoId($id))),false);
            if (count($rows)==0) {echo $empty;return;}
            $pid = '';
            if (!array_key_exists('ParentExecJobID',$rows[0])) {
                $pid = $id;
            } else {
                $pid = $rows[0]['ParentExecJobID'];
                $rows = iterator_to_array($DB->ExecJob->find(array('_id' => new MongoId($pid))),false);
            }
            $rows2 = $DB->ExecJob->find(array('ParentExecJobID' => $pid));
            echo json_encode(array_merge($rows,iterator_to_array($rows2,false)));
        } else if ($op == 'getExecJobFlow') {
            $id = $data->id;
            $tids = array();
            $mtids = array();
            $fids = array();
            array_push($fids,$id);
            array_push($tids,$id);
            array_push($mtids,new MongoId($id));
            $hasFlow = false;
            do {
                $rows = $DB->ExecJobFlow->find(array('ParentExecJobFlowID' => array('$in' =>$fids)),array('_id' => true));
                $hasFlow = ($rows->hasNext());
                $fids = array();
                foreach ($rows as $r) {
                    array_push($tids,(string)$r['_id']);
                    array_push($fids,(string)$r['_id']);
                    array_push($mtids,$r['_id']);
                }
            } while ($hasFlow);
            //$DB->ExecJob->remove(array('ParentExecJobFlowID' => array('$in' => $tids)));
            //$DB->ExecJobFlow->remove(array('_id' => array('$in' => $mtids)));
            $rows = $DB->ExecJobFlow->find(array('_id' => array('$in' => $mtids))
                                       ,array('Log' => false,'RunHistory' => false));
            $rows2 = $DB->ExecJob->find(array('ParentExecJobFlowID' => array('$in' => $tids))
                                       ,array('RunHistory' => false,'HostCommandList' => false));
            $recs = array();
            if ($rows->hasNext()){
               $recs = iterator_to_array($rows,false);
            }
            echo json_encode(array_merge($recs,iterator_to_array($rows2,false)));
        }  else if ($op == 'getFlowName') {
            $id = $data->id;
			$rows = $DB->ExecJobFlow->find(array('ParentExecJobFlowID' => $id));

//fwrite($file,"getFlowName id=" . $id."\n");
			foreach ($rows as $r) {
				$level1_fid = (string)$r['_id'];
				$JobFlowID = (string)$r['JobFlowID'];
//fwrite($file,"getFlowName level1_fid=" . $level1_fid."\n");
//fwrite($file,"getFlowName JobFlowID=" . $JobFlowID."\n");
			}
			$rows2 = $DB->JobFlow->find(array('_id' => $JobFlowID));  
			foreach ($rows2 as $r) {
				$Name = (string)$r['Name'];
//fwrite($file,"getFlowName Name=" . $Name."\n");
			}

            echo json_encode(iterator_to_array($rows2,false));
        } else if ($op == 'getFirstLevelExecJobFlow') {
            $id = $data->id;
//fwrite($file,"id=" . $id ."\n");
			//$mtids = array();
			$rows = $DB->ExecJobFlow->find(array('ParentExecJobFlowID' => $id));


			foreach ($rows as $r) {
				$level1_fid = (string)$r['_id'];
				//array_push($mtids,$r['_id']);
			}
//fwrite($file,"level1_fid=" . $level1_fid."\n");
			$rows2 = $DB->ExecJobFlow->find(array('ParentExecJobFlowID' => $level1_fid))->sort(array('JobFlowID' => 1)); //sort(array('Minor' => 1));  
			
			foreach ($rows2 as $r) {
				$mtids = (string)$r['_id'];
				$Minor = $r['Minor'];
				//array_push($mtids,$r['_id']);
//fwrite($file,"getFirstLevelExecJobFlow  mtids=" . $mtids.",minor=" . $Minor ."\n");
			}
            echo json_encode(iterator_to_array($rows2,false));
        } else if ($op == 'getSecondLevelExecJobFlow') {
            $id = $data->id;
//fwrite($file,"getSecondLevelExecJobFlow id=" . $id."\n");

			//$mtids = array();
			$rows = $DB->ExecJobFlow->find(array('ParentExecJobFlowID' => $id));
			foreach ($rows as $r) {
				$level1_fid = (string)$r['_id'];
				//array_push($mtids,$r['_id']);
			}
//fwrite($file,"level1_fid=" . $level1_fid."\n");
			//$rows2 = $DB->ExecJobFlow->find(array('$and' => array(array('ParentExecJobFlowID' => $level1_fid),array('State' => 'Running')) ));

			$rows2 = iterator_to_array($DB->ExecJobFlow->find(array('ParentExecJobFlowID' => $level1_fid))->sort(array('JobFlowID' => 1)),false);
			
			$cur_fid = "";
			$num_finish = 0;
			$num_wait = 0;
			$num_row = count($rows2);
		
			for($i=0;$i<$num_row;$i++) {
				$snd_level_id = (string)$rows2[$i]['_id'];
				$state = $rows2[$i]['State'];
				//$num_row = $num_row + 1;
//fwrite($file,"snd_level_id=" . $snd_level_id.";state=" .$state."\n");
				if ($state == 'Running'){
					$cur_fid = $snd_level_id;
					break;
				}else if ($state == 'Wait'){
					$num_wait = $num_wait + 1;
				}else if ($state == 'Finish'){
					$num_finish = $num_finish + 1;
				}
			}
//fwrite($file,"num_wait=" . $num_wait."\n");
//fwrite($file,"num_finish=" . $num_finish."\n");
//fwrite($file,"num_row=" . $num_row."\n");

			if (strlen($cur_fid) == 0){
				if ($num_wait == $num_row){
					$cur_fid = (string)$rows2[0]['_id'];
				}
				if ($num_finish == $num_row){
					//$cur_fid = (string)$rows2[$num_row-1]['_id'];
					$cur_fid = $snd_level_id;
				}				
			}

//fwrite($file,"cur_fid=" . $cur_fid."\n");
			$rows3 = $DB->ExecJobFlow->find(array('ParentExecJobFlowID' => $cur_fid));
			foreach ($rows3 as $r) {
				$snd_level_mtids = (string)$r['_id'];
//fwrite($file,"snd_level_mtids=" . $snd_level_mtids."\n");
			}

			$rows4 = $DB->ExecJobFlow->find(array('ParentExecJobFlowID' => $snd_level_mtids))->sort(array('JobFlowID' => 1));
			foreach ($rows4 as $r) {
				$snd_level_mtids = (string)$r['_id'];
//fwrite($file,"finally snd_level_mtids=" . $snd_level_mtids."\n");
			}

            echo json_encode(iterator_to_array($rows4,false));
        } else if ($op == 'clearexecjobflow') {
            $id = $data->id;
            $tids = array();
            $mtids = array();
            $fids = array();
            array_push($fids,$id);
            array_push($tids,$id);
            array_push($mtids,new MongoId($id));
            $hasFlow = false;
            do {
                $rows = $DB->ExecJobFlow->find(array('ParentExecJobFlowID' => array('$in' =>$fids)),array('_id' => true));
                $hasFlow = ($rows->hasNext());
                $fids = array();
                foreach ($rows as $r) {
                    array_push($tids,(string)$r['_id']);
                    array_push($fids,(string)$r['_id']);
                    array_push($mtids,$r['_id']);
                }
            } while ($hasFlow);
            $DB->ExecJob->remove(array('ParentExecJobFlowID' => array('$in' => $tids)));
            $DB->ExecJobFlow->remove(array('_id' => array('$in' => $mtids)));
            echo json_encode($tids);
        } else if ($op == 'loadjobflows') {
            $nodeids = $data->nodeids;
            $rows = $DB->ExecJobFlow->find(array('$and' => array(array('ObjectTreeID' => array('$in' => $nodeids)),array("ParentExecJobFlowID" => array('$exists' => false))))
                                       ,array('Log' => false,'RunHistory' => false));
            //$rows = $DB->ExecJobFlow->find(array('ObjectTreeID' => array('$in' => $nodeids)));
            echo json_encode(iterator_to_array($rows,false));
        } else if ($op == 'getObjectJobs') {
            $objectids = $data->objectids;
            $jobstatus = $data->status;
            $rows = $DB->ExecJob->find(array('$and' => array(array('ObjectID' => array('$in' =>$objectids)),
                                    array('State' => array( '$in' => $jobstatus )),
                                    array("ParentExecJobFlowID" => array('$exists' => false))))
                                       ,array('Log' => false,'RunHistory' => false));
            $recs = array();
            if ($rows->hasNext()){
               $recs = iterator_to_array($rows,false);
            }
            echo json_encode($recs);
        } else if ($op == 'getObjectCmds') {
            $objectids = $data->objectids;
            $rows = $DB->ExecCmd->find(array('ObjectID' => array('$in' =>$objectids)))->sort(array('Time' => -1));
            $recs = array();
            if ($rows->hasNext()){
               $recs = iterator_to_array($rows,false);
            }
            echo json_encode($recs);
        } else if ($op == 'getTreeJobs') {
            $nodeids = $data->nodeids;
            $withchild = (!in_array('withchild',get_object_vars($data))?false:($data->withchild == true));
            $rows = $DB->ExecJob->find(array('ObjectTreeID' => array( '$in' => $nodeids )),array('Log' => false,'RunHistory' => false,'HostCommandPrgs'=>false));
            $recs = array();
            if ($rows->hasNext()){
               $recs = iterator_to_array($rows,false);
            }
            
            if ($withchild) {
                $pids = array();
                foreach($recs as $r) {
                    array_push($pids,$r['_id']->{'$id'});
                }
                
                $rows = $DB->ExecJob->find(array('ParentExecJobID' => array( '$in' => $pids ))
                                           ,array('Log' => false,'RunHistory' => false,'HostCommandPrgs'=>false));
                if ($rows->hasNext()){
                   $recs = array_merge($recs,iterator_to_array($rows,false));
                }
            }
            echo json_encode($recs);
        } else if ($op == 'loadTreeParentJobs') {
            $treeid = $data->treeid;
            $rows = $DB->ObjectTree->find(array('AncestorsID' => $treeid ),array('_id' => true));
            $tids = array($treeid);
            foreach ($rows as $r){
               array_push($tids,$r['_id']);
            }
            $rows2 = $DB->ExecJob->find(array('$and' => array(array('ObjectTreeID' => array('$in' => $tids)),array("ParentExecJobID" => array('$exists' => false))))
                                    ,array('Log' => false,'RunHistory' => false,'HostCommandPrgs'=>false));
            
            echo json_encode(iterator_to_array($rows2,false));
        }else if ($op == 'loadChildJobs') {
            $pid = $data->jobid;
            $rows2 = $DB->ExecJob->find(array('ParentExecJobID' => $pid)
                                    ,array('Log' => false,'RunHistory' => false,'HostCommandPrgs'=>false));
            
            echo json_encode(iterator_to_array($rows2,false));
        } else if ($op == 'getTreeJobFlows') {
            $nodeids = $data->nodeids;
            $withchild = (!in_array('withchild',get_object_vars($data))?false:($data->withchild == true));
            $rows = $DB->ExecJobFlow->find(array('ObjectTreeID' => array( '$in' => $nodeids )));
            $recs = array();
            if ($rows->hasNext()){
               $recs = iterator_to_array($rows,false);
            }
            //get the execjobs in execjobflow
            $pids = array();
            foreach($recs as $r) {
                array_push($pids,$r['_id']->{'$id'});
            }
            $rows = $DB->ExecJob->find(array('ParentExecJobFlowID' => array( '$in' => $pids )),array('Log' => false,'RunHistory' => false));
            if ($rows->hasNext()){
               $recs = array_merge($recs,iterator_to_array($rows,false));
            }

            echo json_encode($recs);
        } else if ($op == 'save') {
            $row = $data->item;
            $DB->ExecJob->save($row);
            dbreturn(0,"OK");
        } else if ($op == 'del') {
            $ids = $data->itemids;
            $DB->ExecJob->remove(array('_id' => array( '$in' => $ids )));
        } else if ($op == 'getjoblog') {
            $jlist = array();
            foreach ($data->jobid as $jid) array_push($jlist,new MongoId($jid));
            $rows = $DB->ExecJob->find(array('_id' => array('$in' => $jlist ))
                    //,array('JobID' => true,'HostStartTime' => true,'AgentIP' => true,'Log' => true,'RunHistory' => true)
                    )->sort(array('HostStartTime' => 1));
            if ($rows->hasNext()){
                echo json_encode(iterator_to_array($rows,false));
            } else {
                echo json_encode($empty);
            }
        } else if ($op == 'getexecstatus') {
            $jlist = array();
            foreach ($data->jobid as $jid) array_push($jlist,new MongoId($jid));
            $rows = $DB->ExecJob->find(array('_id' => array('$in' => $jlist )),array('State' => true));
            $recs = array();
            if ($rows->hasNext()){
               $recs = iterator_to_array($rows,false);
            }            
            $rows = $DB->ExecJobFlow->find(array('_id' => array('$in' => $jlist )),array('State' => true));
            if ($rows->hasNext()){
                $recs = array_merge($recs,iterator_to_array($rows,false));
            }
            echo json_encode($recs);
        }else if ($op == 'execjob') {
            $nodeid = $data->nodeid;
            $jobid = $data->jobid;
            $jobmode = $data->jobmode;
            $userid=$_SESSION['USERID'];
            
            $ret = $redis->lpush("Queue_System","Command=MakeObjectTree_ExecJobs,JobID=$jobid,ObjectTreeID=$nodeid,Type=START,RunMode=$jobmode,User=$userid");
            dbreturn($ret,"Redis lpush return.");
        }else if ($op == 'execjobByObject') {
//fwrite($file," op=" . $op ."\n");
            $objid = $data->objid;
            $jobid = $data->jobid;
            $jobmode = $data->jobmode;
            $userid=$_SESSION['USERID'];
            $redis_cmd = "Command=ExecJob_ByObject,JobID=$jobid,ObjectID=$objid,Type=START,RunMode=$jobmode,User=$userid";
//fwrite($file," redis_cmd=" . $redis_cmd ."\n");

            $ret = $redis->lpush("Queue_System",$redis_cmd);
            dbreturn($ret,"Redis lpush return.");
        }else if ($op == 'stopjob') {
            $jobids = $data->jobid;
            $userid=$_SESSION['USERID'];
            foreach($jobids as $jid) {
                $ret = $redis->lpush("Queue_System","Command=CloseExecJob,ExecJobID=$jid,User=$userid");
            }
            dbreturn(0,"Redis lpush return.");
        } else if ($op == 'startjob') {
            $jobids = $data->jobid;
            $userid=$_SESSION['USERID'];
            foreach($jobids as $jid) {
                $ret = $redis->lpush("Queue_System","Command=StartExecJob,ExecJobID=$jid,User=$userid");
            }
            dbreturn(0,"Redis lpush return.");
        } else if ($op == 'dropjob') {
            $jobids = $data->jobid;
            $userid=$_SESSION['USERID'];
            foreach($jobids as $jid) {
                $ret = $redis->lpush("Queue_System","Command=DropExecJob,ExecJobID=$jid,User=$userid");
            }
            dbreturn(0,"Redis lpush return.");
        } else if ($op == 'execjobflow') {
            $nodeid = $data->nodeid;
            $jobflowid = $data->jobflowid;
            $jobmode = $data->jobmode;
            $userid=$_SESSION['USERID'];
            
            $ret = $redis->lpush("Queue_System","Command=MakeObjectTree_ExecJobFlows,JobFlowID=$jobflowid,ObjectTreeID=$nodeid,Type=START,RunMode=$jobmode,User=$userid");
            dbreturn($ret,"Redis lpush return.");
        } else if ($op == 'resumejobflow') {
            $jobids = $data->jobid;
            $userid=$_SESSION['USERID'];
            foreach($jobids as $jid) {
                $ret = $redis->lpush("Queue_System","Command=FinishByMan,ExecJobID=$jid,User=$userid");
            }
            dbreturn(0,"Redis lpush return.");
        } else if ($op == 'loadjobstatus') {
            $jobids = $data->jobids;
            $mids = array();
            foreach($jobids as $id) {
                array_push($mids,new MongoId($id));
            }
            $rows = $DB->ExecJob->find(array('_id' => array( '$in' => $mids )),array('State' => true));
            if ($rows->hasNext()){
               echo json_encode(iterator_to_array($rows,false));
            }
        } else if ($op == 'loadjobflowstatus') {
            $jobflowids = $data->jobflowids;
            $mids = array();
            foreach($jobflowids as $id) {
                array_push($mids,new MongoId($id));
            }
            $rows = $DB->ExecJobFlow->find(array('_id' => array( '$in' => $mids )),array('State' => true));
            if ($rows->hasNext()){
               echo json_encode(iterator_to_array($rows,false));
            }
        } else if ($op == 'execcommand') {
            $cmd = $data->cmd;
            $DB->ExecCmd->save($cmd);
            $id = $cmd->_id;
            echo $id;
            $userid=$_SESSION['USERID'];
            $ret = $redis->lpush("Queue_System","Command=ExecCmd,ExecCmdID=$id,User=$userid");
        } else if ($op == 'getexeccommand') {
            $id = $data->id;
            $cmds = $DB->ExecCmd->find(array('$id' => (new MongoId($id))));
            if ($cmds->hasNext()){
               echo json_encode(iterator_to_array($cmds,false));
            }
        } else if ($op == 'removecommand') {
            $ids = $data->ids;
            foreach ($ids as $id) {
                $DB->ExecCmd->remove(array('_id' => new MongoId($id)));
            }
        } else echo json_encode($empty);
    } catch (MongoException $e) {
        dbreturn(-2,'Error: ' . $e->getMessage());
    }    
//fclose($file);
?>
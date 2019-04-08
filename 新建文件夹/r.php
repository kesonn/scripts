<?php
    include 'dbconnect.php';
    session_start();
    $userid=$_SESSION['USERID'];    
    $data = json_decode(file_get_contents("php://input"));
    $op = $data->op;

    $empty = array();
    try {
        if ($op == 'getreportlist') {
            //$rows = $DB->Report->find(array('Author' => $userid))->sort(array('Name' => 1));
			$rows = $DB->Report->find()->sort(array('Name' => 1));
            if ($rows->hasNext()){
               echo json_encode(iterator_to_array($rows,false));
            }
        } else if ($op == 'savereport') {
            $row = $data->rpt;
            $DB->Report->save($row);
            dbreturn(0,"OK");
        } else if ($op == 'removereport') {
            $ids = $data->rptids; 	
            $DB->Report->remove(array('_id' => array( '$in' => $ids )));
        } else if ($op == 'gettimereport') {
			unlink("test_report.txt");
$file = fopen("test_report.txt","a");
			$HourSection=array();
fwrite($file, "Key=". json_encode($data->key)."\n");
fwrite($file, "splot=". $data->splot."\n");
			if ($data->splot){
				$rows = $DB->TimeSection->find(array('_id' => $data->splot));
				if ($rows->hasNext()){
					foreach ($rows as $r){					
						$HourSection = $r['Hours'];
					}
				}
			}
fwrite($file, "HourSection=". json_encode($HourSection)."\n");
            $mapFunc = new MongoCode("
function DataMap() {
					var lead2zero = function(a){
						return ('00'+a).slice(-2);
					}
					var checkHour = function(h){
						if (HourSection.length < 1){
							return true;
						}
						var i;
						var rtn = false;
						for (i=0; i<HourSection.length; i++)
							{
							if (h == HourSection[i])
								{
								rtn = true;
								break;
								}
							}
							return(rtn);
					}
                    var d = '';
                    var dt = new Date(this.Time * 1000);

					if (checkHour(dt.getHours())){
						if (timeType == 'min') {
							d = dt.getFullYear()+'/'+lead2zero(dt.getMonth()+1)+'/'+lead2zero(dt.getDate())+' '+lead2zero(dt.getHours())+':'+lead2zero(dt.getMinutes());
						} else if (timeType == 'hour') {
							d = dt.getFullYear()+'/'+lead2zero(dt.getMonth()+1)+'/'+lead2zero(dt.getDate())+' '+lead2zero(dt.getHours());
						} else if (timeType == 'day') {
							d = dt.getFullYear()+'/'+lead2zero(dt.getMonth()+1)+'/'+lead2zero(dt.getDate());
						} else if (timeType == 'week') {
							var X = dt;
							X.setDate( X.getDate() - (7+X.getDay()-1)%7 );
							d = X.getFullYear()+'/'+lead2zero(X.getMonth()+1)+'/'+lead2zero(X.getDate())+' -- ';
							X.setDate( X.getDate() +6);
							d += X.getFullYear()+'/'+lead2zero(X.getMonth()+1)+'/'+lead2zero(X.getDate());
						} else if (timeType == 'month') {
							d = dt.getFullYear()+'/'+lead2zero(dt.getMonth()+1);
						}
						var share={};
						if (hasShare) {
							var f = false;
							var v = this.Value;
							for (var g in groups) {
								share[groups[g].Name] = 0;
								var tmp = groups[g].Value.replace(/@/g,v);
								tmp = tmp.replace(/and/gi,'&&');
								tmp = tmp.replace(/or/gi,'||');
								tmp = tmp.replace(/not/gi,'!');
								f=eval(tmp);                            
								if (f) share[groups[g].Name] = 1;
							}
						}
						emit( d, 
							 {sum: Math.floor(this.Value), 
							  min: Math.floor(this.Value),
							  max: Math.floor(this.Value),
							  count: 1,
							  diff: 0,
							  share: share
						});
					}
                };                                      
            ");
            $reduceFunc = new MongoCode("
                function DataReduce(key, values) {
                    var a = values[0]; // will reduce into here
                    for (var i=1/*!*/; i < values.length; i++){
                        var b = values[i]; // will merge 'b' into 'a'
                        // temp helpers
                        var delta = a.sum/a.count - b.sum/b.count; // a.mean - b.mean
                        var weight = (a.count * b.count)/(a.count + b.count);
                        // do the reducing
                        a.diff += b.diff + delta*delta*weight;
                        a.sum += b.sum;
                        a.count += b.count;
                        a.min = Math.min(a.min, b.min);
                        a.max = Math.max(a.max, b.max);
                        if (hasShare) {
                            for (var g in groups) {
                                a.share[groups[g].Name] += b.share[groups[g].Name];
                            }
                        }
                    }
                    return a;
                };                                        
            ");
            $finFunc = new MongoCode("
                function DataFinalize(key, value){ 
                    value.avg = Math.round(100*value.sum / value.count)/100;
                    value.variance = Math.round(100*value.diff / value.count)/100;
                    value.stddev = Math.round(100*Math.sqrt(value.variance))/100;
                    if (hasShare) {
                        for (var g in groups) {
                            value.share[groups[g].Name] = value.share[groups[g].Name]/value.count;
                        }
                    }
                    return value;
                }                                     
            ");

			$d1 = $data->d1;
            $d2 = $data->d2;
            $command = array(
                'mapreduce' => 'Data',
                'map' => $mapFunc,
                'reduce' => $reduceFunc,
                'finalize' => $finFunc,
                'query' => array(
                    'DataTypeID' => new MongoId($data->key->DataTypeId),
					'Time' => array( '$gt' => $d1, '$lt' => $d2)
                ),
                'scope' => array(
                    'timeType' => ($data->timeType),
                    'hasShare' => in_array("share", $data->key->Aggrs),
                    'groups' => $data->key->Groups,
					'HourSection' => $HourSection
                ),
                'out' => array('inline' => TRUE),
            );        
//fwrite($file, "command=". json_encode($command)."\n");
            $rows = $DB->command($command);


				foreach ($rows as $r){
					fwrite($file, "r=". json_encode($r)."\n");
				}
fclose($file);
            echo json_encode($rows);

        } else if ($op == 'geteventreport') {  // event report
            $objlist = array();
            foreach ($data->objectlist as $key => $value) {
                array_push($objlist,$key);
            }
            $mapFunc['time'] = new MongoCode("
                function DataMap() {
                    var lead2zero = function(a){
                        return ('00'+a).slice(-2);
                    }
                    var d = '';
                    var dt = new Date(this.Time * 1000);
                    if (timeType == 'hour') {
                        d = dt.getFullYear()+'/'+lead2zero(dt.getMonth()+1)+'/'+lead2zero(dt.getDate())+' '+lead2zero(dt.getHours());
                    } else if (timeType == 'day') {
                        d = dt.getFullYear()+'/'+lead2zero(dt.getMonth()+1)+'/'+lead2zero(dt.getDate());
                    } else if (timeType == 'week') {
                        var X = dt;
                        X.setDate( X.getDate() - (7+X.getDay()-1)%7 );
                        d = X.getFullYear()+'/'+lead2zero(X.getMonth()+1)+'/'+lead2zero(X.getDate())+' -- ';
                        X.setDate( X.getDate() +6);
                        d += X.getFullYear()+'/'+lead2zero(X.getMonth()+1)+'/'+lead2zero(X.getDate());
                    } else if (timeType == 'month') {
                        d = dt.getFullYear()+'/'+lead2zero(dt.getMonth()+1);
                    }
                    emit( d, {
                        danger: ((eval(isDanger))?1:0), 
                        warning: ((eval(isWarning))?1:0),
                        info: ((eval(isInfo))?1:0)
                    });
                };                                     
            ");
            $mapFunc['hostip'] = new MongoCode("
                function DataMap() {
                    emit( this.HostIP, {
                        danger: ((eval(isDanger))?1:0), 
                        warning: ((eval(isWarning))?1:0),
                        info: ((eval(isInfo))?1:0)
                    });
                };                                     
            ");
            $mapFunc['object'] = new MongoCode("
                function DataMap() {
                    emit( this.ObjectID, {
                        danger: ((eval(isDanger))?1:0), 
                        warning: ((eval(isWarning))?1:0),
                        info: ((eval(isInfo))?1:0)
                    });
                };                                     
            ");
            $mapFunc['tree'] = new MongoCode("
                function DataMap() {
                    var d=objectIndex[this.ObjectID];  
                    emit(d, {
                        danger: ((eval(isDanger))?1:0), 
                        warning: ((eval(isWarning))?1:0),
                        info: ((eval(isInfo))?1:0)
                    });
                };                                     
            ");
            $mapFunc['closetype'] = new MongoCode("
                function DataMap() {
                    var d='其他';
                    if (this.CloseType != undefined) d = this.CloseType;
                    emit( d, {
                        danger: ((eval(isDanger))?1:0), 
                        warning: ((eval(isWarning))?1:0),
                        info: ((eval(isInfo))?1:0)
                    });
                };                                     
            ");
            $reduceFunc = new MongoCode("
                function DataReduce(key, values) {
                    var a = values[0]; // will reduce into here
                    for (var i=1/*!*/; i < values.length; i++){
                        var b = values[i]; // will merge 'b' into 'a'
                        a.danger += b.danger;
                        a.warning += b.warning;
                        a.info += b.info;
                    }
                    return a;
                };                                        
            ");
            $finFunc = new MongoCode("
                function DataFinalize(key, value){ 
                    return value;
                }                                     
            ");
            
            $l3 = $data->level->l3;
            $l2 = $data->level->l2;
            $d1 = $data->d1;
            $d2 = $data->d2;
            
            $command = array(
                'mapreduce' => 'Event',
                'map' => $mapFunc[$data->reportType],
                'reduce' => $reduceFunc,
                'finalize' => $finFunc,
                
                'query' => array(
                    'ObjectID' => array( '$in' => $objlist ),
                    'Time' => array( '$gt' => $d1, '$lt' => $d2)
                ),
                'scope' => array(
                    'timeType' => ($data->timeType),
                    'objectIndex' => ($data->objectlist),
                    'isDanger' => ("this.Level>$l3"),
                    'isWarning' => ("((this.Level>$l2)&&(this.Level<=$l3))"),
                    'isInfo' => ("this.Level<=$l2")
                ),
                'out' => array('inline' => TRUE),
            ); 

            $rows = $DB->command($command);
            echo json_encode($rows);
        } else echo json_encode($empty);
    } catch (MongoException $e) {
        dbreturn(-2,'Error: ' . $e->getMessage());
    }  
?>
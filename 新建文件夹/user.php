<?php
    include 'dbconnect.php';
    session_start();
    $data = json_decode(file_get_contents("php://input"));
    if (@$_GET['op']) $op = $_GET['op'];
    else $op = $data->op;

    $empty = array();
    try {
        if ($op == 'query') {
            $users = $DB->User->find();
            if ($users->hasNext()){
               echo json_encode(iterator_to_array($users,false));
            }
        } else if ($op == 'querygroup') {
            $groups = $DB->UserGroup->find();
            if ($groups->hasNext()){
               echo json_encode(iterator_to_array($groups,false));
            }
        } else if ($op == 'save') {
            $nrecs = $data->item;
            if (is_array($nrecs)) {
                foreach ($nrecs as $doc) $DB->User->save($doc);
            } else {
                $DB->User->save($nrecs);
            }
        } else if ($op == 'savegroup') {
            $nrecs = $data->item;
            if (is_array($nrecs)) {
                foreach ($nrecs as $doc) $DB->UserGroup->save($doc);
            } else {
                $DB->UserGroup->save($nrecs);
            }
        } else if ($op == 'del') {
            $ids = $data->itemids;
            $DB->User->remove(array('_id' => array( '$in' => $ids )));
        } else if ($op == 'get') {
            $userid = '';
            if (isset($_SESSION['USERID'])) $userid=$_SESSION['USERID'];
            echo $userid;
        } else if ($op == 'login') {
            $username = $data->username;
            $password = $data->password;
            $cond = array('$and' => array(array('_id' => $username),array('Password' => $password)));
            $users = $DB->User->find($cond);
            if (!$users->hasNext()) {
                dbreturn (-1,'用户不存在或者密码错误!');
            } else {
                $usr = $users->getNext();
                $_SESSION['USERID'] = $usr['_id'];
                dbreturn(0,$usr['_id']);
            }
        } else if ($op == 'changepassword') {
            $username = $_SESSION['USERID'];
            $newpw = $data->newpw;
            $password = $data->oldpw;
            $cond = array('$and' => array(array('_id' => $username),array('Password' => $password)));
            $users = $DB->User->find($cond);
            if (!$users->hasNext()) {
                dbreturn (-1,'密码错误!');
            } else {
                $newdata = array('$set' => array("password" => $newpw));
                $DB->User->update(array("_id" => $username), $newdata);
                dbreturn(0,'');
            }
        }else if ($op == 'logout') {
            $_SESSION['USERID'] = '';
            //dbreturn(0,'/');
            //header("location:/");
        } else echo json_encode($empty);
    } catch (MongoException $e) {
        dbreturn(-2,'Error: ' . $e->getMessage());
    }
?>
<?php
    include 'dbconnect.php';
    //ini_set('post_max_size', '64M');
    //ini_set('upload_max_filesize', '64M');
    $grid = $DB->getGridFS();                    // Initialize GridFS

    $fsname='--';
    if(array_key_exists('fsname', $_REQUEST)) $fsname = $_REQUEST["fsname"];
    if(array_key_exists('oldfsname', $_REQUEST)) $oldfsname = $_REQUEST["oldfsname"];
    //$filename = $_REQUEST["filename"];
    try {
        if (isset($oldfsname)) {
            $file = $grid->findOne($oldfsname);
            if ($file) {
                $fileid = $file->file['_id']; 
                $grid->delete($fileid); 
            }
        }
        //$name = $_FILES['file'][ 'tmp_name' ];        // Get Uploaded file name
        //$type = $_FILES['file']['type'];        // Try to get file extension
        echo $fsname;
        $id = $grid->storeUpload('file',$fsname);    // Store uploaded file to GridFS
        exit(0);
    } catch (Exception $e) {
        echo 'error';
        dbreturn(-2,'Error: ' . $e->getMessage());
    }    
?>
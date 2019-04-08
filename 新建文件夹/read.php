<?php
    include 'dbconnect.php';
    try {
        if ( !empty( $_FILES ) ) {
            $tempPath = $_FILES[ 'file' ][ 'tmp_name' ];
            $fext = pathinfo($_FILES[ 'file' ][ 'name' ], PATHINFO_EXTENSION);
            $uploadPath = dirname(dirname( __FILE__ )) . '/app/img/thumb/'."_tmp_.csv";
            //move_uploaded_file( $tempPath, $uploadPath );            
            //$filename = $uploadPath;
            $filename = $tempPath;
            $firstline = true;
            setlocale(LC_ALL, 'zh_CN');
            $handle=fopen($filename,'r');
            echo "[";
            while (($data = fgetcsv($handle, 1000, ",")) !== FALSE){ 
            //while(!feof($handle) && $data=fgets($handle,10000)){
                if (!$firstline) echo ",";
                else $firstline = false;
                $row = array();
                foreach ($data as $d) {

                    array_push($row, iconv('gbk','utf-8',$d));
                }
                echo json_encode($row);
            }
            fclose($handle);
            echo "]";
        } else {
            echo 'No files';
        }  
    } catch (Exception $e) {
        echo 'error';
        dbreturn(-2,'Error: ' . $e->getMessage());
    }    
?>
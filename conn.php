<?php 
	$mysql_host =   	"mysql1.000webhost.com";
	$mysql_database = "a6439806_test";
	$mysql_user = "a6439806_barret";
	$mysql_password = "wangsheng1030";
	$conn = mysql_connect($mysql_host,$mysql_user,$mysql_password);
	if (!$conn) {
		die("Database Connection Error!");				// exception
	}
	mysql_select_db($mysql_database,$conn);
?>
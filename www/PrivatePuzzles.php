<?php 
// if doesn't log in , jump to main puzzle store
// deal with log off function
session_start(); 
	if (!isset($_SESSION['username'])) {
		echo "<script type='text/javascript'>
		window.location.href ='MyOwnPix.php'
		</script>";  
	}
	if (isset($_POST['logoff'])) {
		session_unset();
		echo "<script type='text/javascript'>
			window.location.href ='MyOwnPix.php'
			</script>";	
	}
	if (isset($_POST['deleteId'])) {
		$deletedPuzzle = $_POST['deleteId'];
		include("conn.php");
		$resultSet = mysql_query("select position from Puzzle where id = '{$deletedPuzzle}'");
		$deleteFile = mysql_fetch_row($resultSet);
		$filename = $deleteFile[0];
		unlink($filename);
		$delete = mysql_query("delete from Puzzle where id='{$deletedPuzzle}'");
		$deleteShared = mysql_query("delete from Share where puzzleId='{$deletedPuzzle}'");
		$deleteVotes = mysql_query("delete from Votes where puzzleId='{$deletedPuzzle}'");
		mysql_close();
		unset($_POST['deleteId']);
	}
	if (isset($_POST['shareId'])) {
		$sharedPuzzle = $_POST['shareId'];
		include("conn.php");
		$search = mysql_query("select name,username,position from Puzzle where id ='{$sharedPuzzle}'");
		$shareInfo = mysql_fetch_row($search);
		$insertShare = mysql_query("insert into Share(puzzleId,name,username,position) values('{$sharedPuzzle}','{$shareInfo[0]}','{$shareInfo[1]}','{$shareInfo[2]}')");	
		$insertVotes = mysql_query("insert into Votes(puzzleId,username) values('{$sharedPuzzle}','{$shareInfo[1]}')");
		mysql_close();
		unset($_POST['shareId']);
	}
	if (isset($_POST['stopShareId'])) {
		$stopSharePuzzle = $_POST['stopShareId'];
		include("conn.php");
		$stopShare = mysql_query("delete from Share where puzzleId = '{$stopSharePuzzle}'");		
		mysql_close();
		unset($_POST['stopShareId']);
	}
?>
<html>
<head>
<title>LINK-A-PIX</title>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="shortcut icon" type="image/x-icon" href="images/puzzle.ico" media="screen" />
<LINK HREF="style.css" TYPE="text/css" REL="stylesheet">
<link href="css/PrivatePuzzles.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="js/Popup.js"></script>
<script src="js/jquery.js" ></script>
</head>
<body>
<!-- deal with changing password function -->
<?php 
if (isset($_POST['changePassword'])) {
	echo "<script>
		document.body.onload = topDiv();
	</script>";	
	$old = $_POST['oldPassword'];
	$new = $_POST['newPassword'];
	$newRetype = $_POST['newPasswordRetype'];
	
	if ($old=="" || $new=="" || $newRetype=="") {
		unset( $_POST['oldPassword']);
		unset( $_POST['newPassword']);
		unset( $_POST['newPasswordRetype']);
	}
	else if (strlen($new) < 7) {
		unset( $_POST['oldPassword']);
		unset( $_POST['newPassword']);
		unset( $_POST['newPasswordRetype']);
		echo "<script>
		document.getElementById('alert').innerHTML='* Password Length Less Than 7!';
		</script>";	
	}
	else if ($new != $newRetype) {
		unset( $_POST['oldPassword']);
		unset( $_POST['newPassword']);
		unset( $_POST['newPasswordRetype']);
		echo "<script>
		document.getElementById('alert').innerHTML='* Passwords do not match!';
		</script>";	
	}
	else {
		include("conn.php");
		$rs = mysql_query("select password from Users where username = '{$_SESSION['username']}'");
		$result = mysql_fetch_row($rs);
	
		if ($old == $result[0]) {
			mysql_query("update Users set password = '{$new}' where username = '{$_SESSION['username']}'");
			mysql_close();
			echo "<script>
			document.getElementById('alert').innerHTML='* Password is Changed';
			</script>";	
		}
		else {
			mysql_close();
			echo "<script>
			document.getElementById('alert').innerHTML='* Old Password Is Incorrect !';
			</script>";	
		}
		unset( $_POST['oldPassword']);
		unset( $_POST['newPassword']);
		unset( $_POST['newPasswordRetype']);
	}	
}
?>

<!-- header -->
<table width="100%" height="100%"  border="0" cellpadding="0" cellspacing="0" background="images/rep_1.jpg">
  <tr>
    <td>&nbsp;</td>
    <td width="700" align="left" valign="top">
    <div style="padding-left:0px; padding-top:39px">
      <table width="700" height="800" border="0" cellspacing="0" cellpadding="0">
        <tr>
          <td align="left" valign="top" bgcolor="#FFFFFF" style="border:1px solid #C5C5C5 ">
          <table width="700"  border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td height="199" align="left" valign="top"><table width="700" height="199"  border="0" cellpadding="0" cellspacing="0">
                <tr align="left" valign="top">
                  <td width="495">
                  <div>
                  <a href="index.html"><img src="images/top_1.png" width="462" height="105"></a>
                  </div>
                  <div style="margin:50px 0 0 0" align="center">
<form method="get" name="search">
<table border="0" cellpadding="0" cellspacing="0" class="tab_search">
<tr>
<td>
<input type="text" name="q" title="Search" class="searchinput" id="searchinput" onKeyDown="if (event.keyCode==13) {}" onBlur="if(this.value=='')value='- Search -';" onFocus="if(this.value=='- Search -')value='';" value="- Search -" size="10" style="width:250px;height:30px"/>
</td>
<td>
<input type="image" class="searchaction" onClick="if(document.forms['search'].searchinput.value=='- Search -')document.forms['search'].searchinput.value='';" src="images/submit.jpg"  hspace="2" border="0"/>

</td>
</tr>
</table>
</form>
                  </div>
                  </td>
                  <td><table width="198" border="0" cellspacing="0" cellpadding="0" >
                    <tr align="left" valign="top">
                      <td width="41"><img src="images/main_2.jpg" width="39" height="182" border="0"></td>
                      <td width="40"><img src="images/about_2.jpg" width="38" height="182" border="0"></td>
                      <td width="39"><img src="images/portfolio_2.jpg" width="37" height="182" border="0"></td>
                      <td width="40"><img src="images/services_2.jpg" width="38" height="182" border="0"></td>
                      <td><img src="images/contacts_2.jpg" width="38" height="182" border="0"></td>
                    </tr>
                  </table></td>
                </tr>
              </table>
              <hr />
              </td>
            </tr>
            <tr>
              <td height="536" align="left" valign="top" background="images/back_4.jpg" style="border-top:12px solid #ffffff;background-repeat:no-repeat; background-position:bottom right ; background-repeat:no-repeat">
              <table width="700" height="556"border="0" cellspacing="0" cellpadding="0">
                <tr align="left" valign="top">
                  <td width="438" height="100%" background="images/rep_2.jpg" style="background-position:top right; background-repeat:repeat-y ">
                  <div style="font-size:36px; margin-left:5px">Private Puzzles</div>
                  <div>
	<table border="0" cellspacing="0" cellpadding="0">
    <tr align="center">

<!-- Load puzzle information -->
<?php
   	include("conn.php");
	if(empty($_GET["q"])){
		$sql = mysql_query("select * from Puzzle where username ='{$_SESSION['username']}'");
	}
	else {
		$search = trim($_GET["q"]);
		$sql = mysql_query("select * from Puzzle where name like '%$search%' AND username ='{$_SESSION['username']}'");
	}
    $pagesize = 9; 
    $sum = mysql_num_rows($sql); 
    $count = ceil($sum/$pagesize);
    $lastPage = $count;
    $init = 1;
    $page_len = 3;
    $max_p = $count;    
    if(empty($_GET["page"]) || $_GET["page"]<0){
        $page = 1;
    }else{
        $page = $_GET["page"];
    }
    $off = ($page-1)*$pagesize; 
	
	if(empty($_GET["q"])){
		$content = mysql_query("select name,position,id from Puzzle where username ='{$_SESSION['username']}' order by id limit $off,$pagesize");
	}
	else {
		$content = mysql_query("select name,position,id from Puzzle where name like '%$search%' AND username ='{$_SESSION['username']}' order by id limit $off,$pagesize");
	}
	
	for ($i=0;$i<9;$i++) {
		if ($result = mysql_fetch_array($content)) {
			if ($i!=0 && $i%3==0) {
				echo "</tr><tr align='center'>";	
			}
?>	

<td width="146" height="166" align="center" style="overflow:hidden">
<div style='position:relative ; margin:0 auto 5px auto;height:130px;width:146px; overflow:hidden' onMouseOver="appear('#up<?php echo $result[2] ?>')" onMouseOut="disappear('#up<?php echo $result[2] ?>')" >

<div style="position:absolute;top:0px;height:130px; width:146px;"><a href="GamePlay.php?puzzleId=<?php echo $result[2] ?>" class="buttonEffect"><img height="130" width="140" src="<?php echo $result[1]?>" alt="thumbnail" /></a>
</div>

<div class="toolbar" align="right" id="up<?php echo $result[2] ?>">

<form method="post" id="delete<?php echo "{$result[2]}" ?>" style=" position:absolute; bottom:-14px ; right:15px">
<input type="hidden" value="<?php echo $result[2]; ?>" name="deleteId" />
<a href="###" onClick="deletePuzzle('delete<?php echo "{$result[2]}" ?>')"><img src="images/delete.png" alt="delete" title="delete" /></a>
</form>

<?php 
$rs = mysql_query("select * from Share where puzzleID = '$result[2]'");
$num = mysql_num_rows($rs);
if ($num <= 0) {
?>
<form method="post" id="share<?php echo "{$result[2]}" ?>" style=" position:absolute; bottom:-14px ; right:60px">
<input type="hidden" value="<?php echo $result[2]; ?>" name="shareId" />
<a href="###" onClick="sharePuzzle('share<?php echo "{$result[2]}" ?>')"><img src="images/share.png" alt="share" title="share" /></a>
</form>
<?php
}
else {
?>
<form method="post" id="stopShare<?php echo "{$result[2]}" ?>" style=" position:absolute; bottom:-14px ; right:60px">
<input type="hidden" value="<?php echo $result[2]; ?>" name="stopShareId" />
<a href="###" onClick="stopShare('stopShare<?php echo "{$result[2]}" ?>')"><img src="images/stop_share.png" alt="stop_share" title="stop sharing" /></a>
</form>
<?php 
}
$voteCount = mysql_query("select * from Votes where puzzleId = '{$result[2]}'");
$totalVote = mysql_num_rows($voteCount);
if ($totalVote > 0) {
	$totalVote = $totalVote -1;
}
?>

<div style="position:absolute; bottom:3px ; right:120px">
<img src="images/vote.png" title="votes" /></div>
<div style=" color:#000; position:absolute; bottom:2px; right:<?php if ($totalVote < 10) echo "95px"; else if ($totalVote < 100) echo "88px"; else echo "81px"; ?>"><?php if ($totalVote < 100) echo "(".$totalVote.")"; else echo "(99+)"; ?></div>
</div>

</div>
<?php echo $result[0] ?>
</td>		

<?php				
		}
		else {
			if ($i==0) {
				echo "<p align='center'>Sorry . No Result !</p>";
				break;	
			}
			if ($i!=0 && $i%3==0) {
				echo "</tr><tr>";	
			}
			echo "<td width='136' height='166'>&nbsp;</td>";	
		}
	}

    $page_len = ($page_len%2)?$page_len:$page_len+1;
    $pageoffset = ($page_len-1)/2;
	$url = $_SERVER['REQUEST_URI'];
	$url = parse_url($uri);
	$url = $url[path];
    if($page!=1){
        $key.="<span><a href=\"".$url."?page=1"."\">First</a></span>&nbsp;&nbsp;";
        $key.="<span><a href=\"".$url."?page=".($page-1)."\">Previous</a></span>&nbsp;";
    }else{
        $key.="<span>First</span>&nbsp;&nbsp;";
        $key.="<span>Previous</span>&nbsp;";
    }
    if($lastPage>$page_len){
        if($page<=$pageoffset){
            $init=1;
            $max_p = $page_len;
        }else{
            if($page+$pageoffset>=$lastPage+1){
                $init = $lastPage - $page_len+1;
            }else{
                $init = $page-$pageoffset;
                $max_p = $page + $pageoffset;
            }
        }
    }
    for($i=$init;$i<=$max_p;$i++){
        if($i==$page){
            $key.="&nbsp;[&nbsp;".$i."&nbsp;]&nbsp;";    
        }
		else{
            $key.="&nbsp;<a href=\"".$url."?page=".$i."\">$i</a>&nbsp;";
        }
    }
    if($page < $lastPage){
        $key.="&nbsp;<span><a href=\"".$url."?page=".($page+1)."\">Next</a></span>&nbsp;";
        $key.="&nbsp;<span><a href=\"".$url."?page=".$lastPage."\">Last</a></span>&nbsp;";
    }else{
        $key.="&nbsp;<span>Next</span>&nbsp;";
        $key.="&nbsp;<span>Last</span>&nbsp;";
    }
	$key .= "&nbsp;Page ".$page." / ".$count;
	if ($count==0) {
		$key ="";	
	}
	mysql_close();
?>

</tr>
</table>
</div>

<div align="center" style="padding-top:5px"><?php echo $key; ?></div>
</td>

<!-- User System -->
<td width="262" height="100%">
<div style=" background:url(images/window.png) no-repeat;height:130px">
<br />
<br />
<p align="center" style="margin-top:0px">
Pick A Puzzle<br/>
Load A Puzzle<br />
Play A Puzzle<br />
Log In to Find More !<br />
</p>
</div>
<div class="form">

<h1 style="margin-left:10px">Welcome</h1>
<p align="center"><?php echo $_SESSION['username'] ?></p>
<div style="height:200px;margin:0 20%">
<table width="100%" height="200px">
	<tr>
		<td align="center">
			<a href="GeneralPuzzles.php" class="buttonEffect"><img src="images/SystemPuzzles.png" alt="general" title="General Puzzles" align="top" ></a>			
		</td>
        <td align="center">
			<a href="UserUploadedPuzzles.php" class="buttonEffect"><img src="images/UserUploadedPuzzles.png" alt="UserUploadedPuzzles" title="Uploaded Puzzles" align="top" ></a>
        </td>
	</tr>
    <tr>
    	<td align="center">
        	<a href="Upload.php" class="buttonEffect"><img src="images/upload.png" alt="Upload" title="Upload your favourite" align="top" ></a>
        </td>
        <td align="center">
        	<a href="#" onClick="topDiv();return false" class="buttonEffect"><img src="images/lock.png" alt="password" title="Change Password" align="top" ></a>    
        </td>
    </tr>
    <tr>
        <td align="center" colspan="2">
        	<form method="post">
<input type="submit" alt="logoff" name="logoff" id="logoff" value="" title="Log Off" />
</form>
        </td>
    </tr>
</table>
</div>
</div>
                  </td>
                </tr>
              </table></td>
            </tr>
          </table></td>
        </tr>
      </table>
    </div>
    <div style="border: 1px solid #C5C5C5; margin-top:3px; padding-left:40%">
    	<img src="images/footer.png" alt="Link A Pix" style="margin-top:2px;margin-left:30px" />
    	<br />
   		<a href="About.html">Find out more about us</a>
    </div>      
  </td>
    <td>&nbsp;</td>
  </tr>
</table>

<script type="text/javascript">
function deletePuzzle(id){
	var flag = confirm("Do you want to delete this puzzle ?");
 	if(flag){
		document.getElementById(id).submit();
 	}
}
function sharePuzzle(id){
	var flag = confirm("Do you want to share this puzzle ?");
 	if(flag){
		document.getElementById(id).submit();
 	}
}
function stopShare(id){
	var flag = confirm("Do you want to stop sharing this puzzle ?");
 	if(flag){
		document.getElementById(id).submit(); 	
	}
}
</script>

<script>
function appear(id) {
	$(id).animate({top:110},{queue: false, duration: 250});
	}
function disappear(id) {
	$(id).animate({top:130},{queue: false, duration: 250});
	}
</script>
</body>
</html>

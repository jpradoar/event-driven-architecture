<?php
$db_host = getenv('MARIADB_HOST');
$db_name = getenv('MARIADB_DATABASE');
$db_user = getenv('MARIADB_USER');
$db_pass = getenv('MARIADB_PASSWORD');
try{
  $db_con = new PDO("mysql:host={$db_host};dbname={$db_name}",$db_user,$db_pass);
  $db_con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}
catch(PDOException $e){
  echo $e->getMessage();
}
$stmt = $db_con->prepare("SELECT * FROM clients");
$stmt->execute();
?>
<!DOCTYPE html>
<html>
<head>

<style>
body {
    font-family: Arial, sans-serif;
    background-color: #35495e;
}
#customers th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #0A5D6E;
  color: white;
}
#customers {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 50%;
  text-align: center;
  background-color: #C3BBBB;
  
}
#customers td, #customers th {
  border: 1px solid #ddd;
  padding: 8px;
}
#customers tr:nth-child(even){background-color: #C3BBBB;}
#customers tr:hover {background-color: #ddd;}
</style>

</head>
<body>
<div align="center">
  <img src="it-infrastructure-icon-28.jpg" height="60" width="60">
  <br>
  <h3>Database clients created by MQTT-Event</h3>
  <table id="customers">
  <tr>
    <th scope="col"> ID </th>
    <th scope="col"> Client</th>
    <th scope="col"> ArchType</th>
    <th scope="col"> Hardware</th>
    <th scope="col"> Product</th>
    <th scope="col"> Deployed</th>
  </tr>
  <?php while($row=$stmt->fetch(PDO::FETCH_ASSOC)) { ?>
    <tr>
    <td><?php echo $row['id']; ?></td>
    <td><?php echo $row['client']; ?></td>
    <td><?php echo $row['archtype']; ?></td>
    <td><?php echo $row['hardware']; ?></td>
    <td><?php echo $row['product']; ?></td>
    <td><?php echo $row['xdate']; ?></td>
    </tr>
  <?php   }   $stmt = null; ?>
  </table>
</div>
</body>
</html> 

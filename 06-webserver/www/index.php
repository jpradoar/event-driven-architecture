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
<meta charset="UTF-8">
<title>Database clients created by MQTT-Event</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
  body {
      font-family: Arial, sans-serif;
      background-color: #f2f2f2;
  }
  .container {
      max-width: 95%;
      margin: 20px auto;
      background-color: #e0e5e8;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
      padding: 20px;
  }
  table {
      border-collapse: collapse;
      margin: 25px 0;
      font-family: Arial, sans-serif;
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
  }
  th, td {
      padding: 12px 15px;
      text-align: left;
      border-bottom: 1px solid #ddd;
  }
  th {
      background-color: #4CAF50;
      color: white;
  }
</style>
</head>
<body>
<div class="container">
    <div align="center">
        <img src="it-infrastructure-icon-28.jpg" height="60" width="60">
        <h3>Database clients created by MQTT-Event v1</h3>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Client</th>
                    <th>ArchType</th>
                    <th>Hardware</th>
                    <th>Product</th>
                    <th>Deployed</th>
                    <th>License type</th>
                </tr>
            </thead>
            <tbody>
                <?php while($row = $stmt->fetch(PDO::FETCH_ASSOC)) { ?>
                    <tr>
                        <td><?php echo $row['id']; ?></td>
                        <td><?php echo $row['client']; ?></td>
                        <td><?php echo $row['archtype']; ?></td>
                        <td><?php echo $row['hardware']; ?></td>
                        <td><?php echo $row['product']; ?></td>
                        <td><?php echo $row['xdate']; ?></td>
                        <td><?php echo $row['license']; ?></td>
                    </tr>
                <?php } ?>
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
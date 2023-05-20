<?php
$servername   = "mariadb";
$username     = "admin";
$password     = "admin";
$dbname       = "clients";

try {
    $db_con = new PDO("mysql:host=$servername;dbname=$dbname;charset=utf8mb4", $username, $password);
    $db_con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Prepare and execute the query
    $stmt = $db_con->prepare("SELECT * FROM clients");
    $stmt->execute();
    
    // Fetch all the results as an associative array
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
    exit(); // Terminate the script if there's a connection error
}
?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    table {
      border-collapse: collapse;
      width: 100%;
    }
    th, td {
      border: 1px solid black;
      padding: 8px;
      text-align: left;
    }
  </style>
</head>
<body>    
  <div align="center">
    <img src="it-infrastructure-icon-28.jpg" height="60" width="60">
    <br><h3>Database clients created by MQTT-Event</h3>
    <table>
      <tr>
        <th>ID</th>
        <th>Client</th>
        <th>ArchType</th>
        <th>Hardware</th>
        <th>Product</th>
        <th>Deployed</th>
        <th>License type</th>
      </tr>
      <?php foreach ($results as $row) { ?>
        <tr>
          <td><?php echo htmlspecialchars($row['id']); ?></td>
          <td><?php echo htmlspecialchars($row['client']); ?></td>
          <td><?php echo htmlspecialchars($row['archtype']); ?></td>
          <td><?php echo htmlspecialchars($row['hardware']); ?></td>    
          <td><?php echo htmlspecialchars($row['product']); ?></td>  
          <td><?php echo htmlspecialchars($row['xdate']); ?></td>
          <td><?php echo htmlspecialchars($row['license']); ?></td>    
        </tr>
      <?php } ?>
    </table>                        
  </div>
</body>
</html>
<?php
$db_host = "mariadb";
$db_name = "clients";
$db_user = "admin";
$db_pass = "admin";
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
<style>
input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
input[type=submit] {
  width: 100%;
  background-color: #4CAF50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
input[type=submit]:hover {
  background-color: #45a049;
}
div {
  border-radius: 5px;
  padding: 20px;
}
body {
  background-color: #f2f2f2;
}
.table {
    border-collapse: collapse;
    margin: 25px 0;
    font-size: 0.9em;
    font-family: sans-serif;
    min-width: 400px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}
.table th,
.table td {
    padding: 1% 15px;
}
.table tbody tr:last-of-type {
    border-bottom: 2px solid #3383FF;
}
#messages {
  border: 1px solid black;
  padding: 10px;
  margin-top: auto;
  max-height: auto;
  overflow: auto;
}
</style>
<head>
  <meta charset="UTF-8">
</head>
<body>    
<div align="center">
<img src="it-infrastructure-icon-28.jpg" height="60" width="60">
<br><h3>Database clients created by MQTT-Event</h3>
<table border="1" class="table">
<tr>
  <th scope="col"> ID </th>
  <th scope="col"> Client</th>
  <th scope="col"> ArchType</th>
  <th scope="col"> Hardware</th>
  <th scope="col"> Product</th>
  <th scope="col"> Deployed</th>
  <th scope="col"> License type</th>
</tr>
<?php while($row=$stmt->fetch(PDO::FETCH_ASSOC)) { ?>
  <tr>
  <td><?php echo $row['id']; ?></td>
  <td><?php echo $row['client']; ?></td>
  <td><?php echo $row['archtype']; ?></td>
  <td><?php echo $row['hardware']; ?></td>    
  <td><?php echo $row['product']; ?></td>  
  <td><?php echo $row['xdate']; ?></td>
  <td><?php echo $row['license']; ?></td>           
  </tr>
<?php   }   $stmt = null; ?>
</table>                        

<br><br><h3>DEPLOYMENT REAL TIME STATUS</h3>
<ul id="messages"></ul>
<script>
  // Conexión a RabbitMQ
  const QUEUE_NAME = 'event-status';
  const AMQP_URL = 'ws://rabbitmq:15674/ws'; // Reemplazar con la URL de conexión a RabbitMQ

  const client = Stomp.client(AMQP_URL);
  client.connect('admin', 'admin', onConnect, onError);

  function onConnect() {
    console.log('Conectado a RabbitMQ');
    client.subscribe(QUEUE_NAME, onMessageReceived);
  }

  function onError(error) {
    console.error('Error de conexión a RabbitMQ:', error);
  }

  function onMessageReceived(message) {
    const body = JSON.parse(message.body);
    console.log('Mensaje recibido:', body);
    const li = document.createElement('li');
    li.innerText = JSON.stringify(body);
    document.getElementById('messages').appendChild(li);
  }
</script>

</div>

</body>
</html>

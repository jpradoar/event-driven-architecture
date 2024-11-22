<?php
// Variables de entorno
$db_host = getenv('MARIADB_HOST');
$db_name = getenv('MARIADB_DATABASE');
$db_user = getenv('MARIADB_USER');
$db_pass = getenv('MARIADB_PASSWORD');

try {
    // Conexión a la base de datos utilizando PDO
    $db_con = new PDO("mysql:host={$db_host};dbname={$db_name};charset=utf8", $db_user, $db_pass);
    $db_con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    // Manejo de errores de conexión
    echo "Error de conexión a la base de datos: " . htmlspecialchars($e->getMessage());
    exit;
}

// Preparar y ejecutar la consulta
try {
    $stmt = $db_con->prepare("SELECT * FROM clients");
    $stmt->execute();
} catch (PDOException $e) {
    echo "Error al ejecutar la consulta: " . htmlspecialchars($e->getMessage());
    exit;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clientes en la Base de Datos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #35495e;
            color: #ffffff;
        }
        #customers {
            font-family: Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
            text-align: center;
            background-color: #C3BBBB;
        }
        #customers th {
            padding: 12px;
            background-color: #0A5D6E;
            color: white;
        }
        #customers td, #customers th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        #customers tr:nth-child(even) {
            background-color: #C3BBBB;
        }
        #customers tr:hover {
            background-color: #ddd;
        }
        #header {
            text-align: center;
            margin-bottom: 20px;
        }
        #header img {
            height: 60px;
            width: 60px;
        }
        #header h3 {
            margin: 10px 0 0 0;
        }
    </style>
</head>
<body>
    <div id="header">
        <img src="it-infrastructure-icon-28.jpg" alt="Icono">
        <h3>Database clients created by MQTT-Event</h3>
    </div>
    <table id="customers">
        <tr>
            <th>ID</th>
            <th>Client</th>
            <th>ArchType</th>
            <th>Hardware</th>
            <th>Product</th>
            <th>Deployed</th>
        </tr>
        <?php while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { ?>
            <tr>
                <td><?php echo htmlspecialchars($row['id']); ?></td>
                <td><?php echo htmlspecialchars($row['client']); ?></td>
                <td><?php echo htmlspecialchars($row['archtype']); ?></td>
                <td><?php echo htmlspecialchars($row['hardware']); ?></td>
                <td><?php echo htmlspecialchars($row['product']); ?></td>
                <td><?php echo htmlspecialchars($row['xdate']); ?></td>
            </tr>
        <?php } ?>
    </table>
</body>
</html>
<?php
// Liberar recursos
$stmt = null;
$db_con = null;
?>

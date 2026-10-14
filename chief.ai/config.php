<?php
    // Database connection details
    $host = "localhost";  // Replace with your PostgreSQL host
    $port = "5432";       // Default PostgreSQL port
    $dbname = "chiefai"; // Replace with your PostgreSQL database name
    $user = "postgres";   // Replace with your PostgreSQL username
    $password = "1234"; // Replace with your PostgreSQL password

    // Create connection string
    $connection_string = "host=$host port=$port dbname=$dbname user=$user password=$password";

    // Establish a connection
    $con = pg_connect($connection_string);

    // Check if the connection was successful
    if (!$con) {
        die("Connection to the database failed: " . pg_last_error());
    }
    echo "Success connecting to the PostgreSQL database";
?>



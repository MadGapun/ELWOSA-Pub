<?php
// Database configuration
$DB_HOST = getenv('ELWOSA_DB_HOST') ?: '192.168.178.200';
$DB_NAME = getenv('ELWOSA_DB_NAME') ?: 'elwosa_pm';
$DB_USER = getenv('ELWOSA_DB_USER') ?: 'postgres';
$DB_PASS = getenv('ELWOSA_DB_PASS') ?: 'claude';  // FIXED: Added missing password
$DB_PORT = getenv('ELWOSA_DB_PORT') ?: '5432';

function get_db_connection() {
    global $DB_HOST, $DB_NAME, $DB_USER, $DB_PASS, $DB_PORT;
    $conn_string = sprintf("host=%s dbname=%s user=%s password=%s port=%s",
        $DB_HOST, $DB_NAME, $DB_USER, $DB_PASS, $DB_PORT);
    $conn = pg_connect($conn_string);
    if (!$conn) {
        http_response_code(500);
        echo json_encode(['error' => 'Database connection failed']);
        exit;
    }
    return $conn;
}
?>
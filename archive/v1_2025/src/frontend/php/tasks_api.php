<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");

require_once 'config.php';

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// OPTION 1: Direct Database Access
function get_tasks_from_db() {
    $conn = get_db_connection();
    $query = "SELECT id, task_id, title, description, status, priority, assigned_to, created_at, estimated_hours, actual_hours FROM tasks ORDER BY id DESC LIMIT 50";
    $result = pg_query($conn, $query);
    
    if (!$result) {
        http_response_code(500);
        echo json_encode(["error" => "Query failed"]);
        exit;
    }
    
    $tasks = [];
    while ($row = pg_fetch_assoc($result)) {
        $tasks[] = $row;
    }
    
    pg_close($conn);
    return $tasks;
}

// OPTION 2: Proxy to Task-API V6 (Recommended)
function get_tasks_from_api() {
    $api_url = "http://192.168.178.200:8001/tasks";
    $context = stream_context_create([
        'http' => [
            'method' => 'GET',
            'timeout' => 10,
            'header' => "Content-Type: application/json\r\n"
        ]
    ]);
    
    $response = file_get_contents($api_url, false, $context);
    
    if ($response === false) {
        // Fallback to database if API is unavailable
        return get_tasks_from_db();
    }
    
    return json_decode($response, true);
}

// Main logic
try {
    $tasks = get_tasks_from_api(); // Try API first, fallback to DB
    echo json_encode($tasks);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Failed to fetch tasks: " . $e->getMessage()]);
}
?>
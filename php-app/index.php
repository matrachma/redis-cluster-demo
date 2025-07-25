<?php
// php-app/index.php
require 'vendor/autoload.php';

// Use Docker service names and the internal port 6379
$parameters = [ 'tcp://redis-1:6379', 'tcp://redis-2:6379', 'tcp://redis-3:6379' ];
$options = ['cluster' => 'redis'];

// Define a fixed array of 16 keys
$redisKeys = [];
for ($i = 1; $i <= 16; $i++) {
    $redisKeys[] = "product:cache:{$i}";
}

// Add a delay to allow the cluster to initialize
sleep(15);
echo "Attempting to connect to Redis Cluster...\n";

try {
    $client = new Predis\Client($parameters, $options);
    echo "✅ PHP App: Successfully connected to Redis Cluster.\n";
} catch (Exception $e) {
    die("🔴 PHP App: Could not connect: " . $e->getMessage() . "\n");
}

$counter = 0;
while (true) {
    try {
        // Cycle through the predefined list of keys
        $keyToUse = $redisKeys[$counter % count($redisKeys)];

        // The value can still be dynamic
        $valueToSet = "data-" . rand(1000, 9999);

        $client->set($keyToUse, $valueToSet);
        $value = $client->get($keyToUse);
        echo "[" . date('H:i:s') . "] PHP App: SET {$keyToUse} to {$value}\n";
        
        $counter++;
        sleep(1);
    } catch (Exception $e) {
        echo "🔴 PHP App: Error during operation: " . $e->getMessage() . ". Retrying...\n";
        sleep(3);
    }
}

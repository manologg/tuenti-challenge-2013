<?php

function get_unique($k) {
    $r = unpack('v*', fread(fopen('/dev/urandom', 'r'),16));
    $uuid = sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
    $r[1], $r[2], $r[3], $r[4] & 0x0fff | 0x4000,
    $r[5] & 0x3fff | 0x8000, $r[6], $r[7], $r[8]);
    return $uuid;
}

$key = '';
$passwd = get_unique($key);
echo " key: " . $key . "\n";
echo " passwd: " . $passwd . "\n";

?>

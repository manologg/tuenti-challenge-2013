<?

function get_unique($k) {
  $r = unpack('v*', fread(fopen('/dev/urandom', 'r'),16));
  $uuid = sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
    $r[1], $r[2], $r[3], $r[4] & 0x0fff | 0x4000,
    $r[5] & 0x3fff | 0x8000, $r[6], $r[7], $r[8]);
  return $uuid;
}

$keys = json_decode(file_get_contents("../data/keys.json"), true);

$_POST["key"] = 'cx1mCcnqzLclMZRDSrwS';
$_POST["pass"] = 'c5a7c4a3-3fc4-4595-92e5-b80404a345c3';

if (isset($_POST["key"]) && isset($_POST["pass"])) {
  $passwd = get_unique($_POST["key"]);
  sleep(5); // no bf this time!

  if (strcmp($passwd, $_POST["pass"]) == 0) {
    echo "welcome master";
    echo "your key: " . $keys[$_POST["key"]];
  }
  else {
    echo "impostor, only the chosen may pass.";
  }
}
else {
  echo "<html><head><title>keyz</title></head><body><form method='POST'>key<input type='text' name='key'><br/>pass<input type='text' name='pass'><br/><input type='submit'>";
}
?>

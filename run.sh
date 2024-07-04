BASE="docker compose -f docker-compose.yml"
$BASE up -d
$BASE exec web /bin/bash
$BASE stop

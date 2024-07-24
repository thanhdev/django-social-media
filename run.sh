BASE="docker compose -f docker-compose.yml"
$BASE up -d --build
$BASE exec web /bin/bash
$BASE stop

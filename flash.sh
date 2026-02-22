#!/usr/bin/env bash
set -euo pipefail

# Change this per device
PORT="${1:-/dev/ttyUSB0}"

echo "==> Using port: $PORT"
echo "==> Removing old files..."
mpremote connect "$PORT" fs rm :main.py || true
mpremote connect "$PORT" fs rm :gps.py || true
mpremote connect "$PORT" fs rm :config.py || true
mpremote connect "$PORT" fs rm :local_orientation.py || true
mpremote connect "$PORT" fs rm :location_calculations.py || true
mpremote connect "$PORT" fs rm :barfindr.py || true
mpremote connect "$PORT" fs rm keys.py || true
mpremote connect "$PORT" fs rm wifi.py || true
mpremote connect "$PORT" fs rm position_adjustment.py || true
mpremote connect "$PORT" fs rm motor_test.py || true

echo "==> Copying new files..."
mpremote connect "$PORT" fs cp main.py :main.py
mpremote connect "$PORT" fs cp gps.py :gps.py
mpremote connect "$PORT" fs cp config.py :config.py
mpremote connect "$PORT" fs cp local_orientation.py :local_orientation.py
mpremote connect "$PORT" fs cp location_calculations.py :location_calculations.py
mpremote connect "$PORT" fs cp barfindr.py :barfindr.py
mpremote connect "$PORT" fs cp keys.py :keys.py
mpremote connect "$PORT" fs cp wifi.py :wifi.py
mpremote connect "$PORT" fs cp position_adjustment.py :position_adjustment.py
mpremote connect "$PORT" fs cp motor_test.py :motor_test.py

# Ensure boot.py won't run surprise stuff
cat > /tmp/boot.py <<'EOF'
# minimal boot.py
EOF
mpremote connect "$PORT" fs cp /tmp/boot.py :boot.py

echo "==> Resetting..."
mpremote connect "$PORT" reset

echo "==> Attaching REPL (Ctrl-] then q to quit mpremote)..."
mpremote connect "$PORT" repl
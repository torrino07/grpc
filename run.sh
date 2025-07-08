#!/bin/bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${ROOT_DIR}/src"

SERVICES=("grpc" "procstat")

echo "🚀 Starting all services from $SRC_DIR"

for service in "${SERVICES[@]}"; do
  SERVICE_PATH="${SRC_DIR}/${service}/run.sh"
  if [[ -x "$SERVICE_PATH" ]]; then
    echo "🟢 Launching $service..."
    (cd "${SRC_DIR}/${service}" && ./run.sh) &
  else
    echo "⚠️ Skipping $service: run.sh not found or not executable at $SERVICE_PATH"
  fi
done

wait
echo "✅ All services are up and running."

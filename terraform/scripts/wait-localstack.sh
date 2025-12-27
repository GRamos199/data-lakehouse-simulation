#!/bin/bash
# Wait for LocalStack to become healthy

echo "Waiting for LocalStack to become healthy..."

for i in $(seq 1 120); do
  RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/health.json http://127.0.0.1:4566/_localstack/health 2>/dev/null || echo "000")
  
  if [ "$RESPONSE" = "200" ]; then
    echo "✓ LocalStack is healthy!"
    cat /tmp/health.json | head -c 200
    echo ""
    exit 0
  fi
  
  echo "Waiting for LocalStack... (attempt $i/120, status: $RESPONSE)"
  sleep 1
done

echo "⚠ Health check timed out, but continuing..."
exit 0

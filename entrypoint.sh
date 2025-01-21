#!/bin/bash
set -e

# Function to wait for a service
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3

    echo "Waiting for $service..."
    while ! nc -z $host $port; do
        echo "$service not available yet - sleeping"
        sleep 2
    done
    echo "$service is up!"
}

# Wait longer for Vault to be ready
wait_for_vault() {
    echo "Waiting for Vault..."
    until curl -fs "${VAULT_ADDR}/v1/sys/health" > /dev/null 2>&1; do
        echo "Vault not ready - sleeping"
        sleep 5
    done
    echo "Vault is up!"
}

# Wait for services
wait_for_service db 5432 "PostgreSQL"
wait_for_vault

# Initialize Vault
echo "Initializing Vault..."
sleep 5  # Give Vault a little more time to be fully ready

# Rest of your initialization...
initialize_vault() {
    # Enable KV secrets engine version 2
    curl --retry 5 --retry-delay 2 -fs -X POST "${VAULT_ADDR}/v1/sys/mounts/secret" \
        -H "X-Vault-Token: ${VAULT_TOKEN}" \
        -d '{"type": "kv", "options": {"version": "2"}}' || echo "KV secrets engine likely already enabled"

    # Store database credentials
    curl --retry 5 --retry-delay 2 -fs -X POST "${VAULT_ADDR}/v1/secret/data/database/credentials" \
        -H "X-Vault-Token: ${VAULT_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{
            \"data\": {
                \"db_name\": \"${DB_NAME}\",
                \"username\": \"${DB_USER}\",
                \"password\": \"${DB_PASSWORD}\",
                \"host\": \"${DB_HOST}\",
                \"port\": \"${DB_PORT}\"
            }
        }" || {
            echo "Failed to store credentials in Vault"
            exit 1
        }
}

initialize_vault

# Make sure directories exist
mkdir -p /app/staticfiles
mkdir -p /app/media

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Start Django
echo "Starting Django..."
python manage.py migrate
exec python manage.py runserver 0.0.0.0:8000

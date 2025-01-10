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

# Function to initialize Vault
initialize_vault() {
    echo "Initializing Vault..."
    
    # Wait for Vault to be unsealed and ready
    until curl -fs "${VAULT_ADDR}/v1/sys/health" > /dev/null 2>&1; do
        echo "Waiting for Vault to be ready..."
        sleep 2
    done
    
    # Enable KV secrets engine version 2
    curl --retry 5 --retry-delay 2 -fs -X POST "${VAULT_ADDR}/v1/sys/mounts/secret" \
        -H "X-Vault-Token: ${VAULT_TOKEN}" \
        -d '{"type": "kv", "options": {"version": "2"}}' || echo "KV secrets engine likely already enabled"
    
    # Store database credentials
    echo "Storing database credentials in Vault..."
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
        
    # Verify credentials were stored
    echo "Verifying credentials storage..."
    curl --retry 5 --retry-delay 2 -fs "${VAULT_ADDR}/v1/secret/data/database/credentials" \
        -H "X-Vault-Token: ${VAULT_TOKEN}" || {
            echo "Failed to verify credentials in Vault"
            exit 1
        }
}

# Wait for services
wait_for_service vault 8200 "Vault"
wait_for_service db 5432 "PostgreSQL"

# Initialize Vault and store credentials
initialize_vault

# Run Django migrations
echo "Running migrations..."
python manage.py migrate

# Start Django app
echo "Starting Django app..."
exec python manage.py runserver 0.0.0.0:8000
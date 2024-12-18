#!/bin/sh
# Wait for Vault
echo "Waiting for Vault..."
while ! nc -z vault 8200; do
  sleep 1
done

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

# Initialize Vault
echo "Initializing Vault..."
curl --retry 5 --retry-delay 5 -X POST "${VAULT_ADDR}/v1/sys/mounts/secret" \
  -H "X-Vault-Token: ${VAULT_TOKEN}" \
  -d '{"type": "kv", "options": {"version": "2"}}'

curl --retry 5 --retry-delay 5 -X POST "${VAULT_ADDR}/v1/secret/data/database/credentials" \
  -H "X-Vault-Token: ${VAULT_TOKEN}" \
  -d "{\"data\": {\"db_name\": \"${DB_NAME}\", \"username\": \"${DB_USER}\", \"password\": \"${DB_PASSWORD}\", \"host\": \"${DB_HOST}\", \"port\": \"${DB_PORT}\"}}"

# Run migrations
python manage.py migrate

# Start Django
python manage.py runserver 0.0.0.0:8000

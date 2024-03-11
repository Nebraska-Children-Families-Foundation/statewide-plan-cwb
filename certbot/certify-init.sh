#!/bin/sh

# Waits for nginx to be available, then gets the first certificate

set -e

until nc -z nginx 80; do
  echo "Waiting for proxy..."
  sleep 5s & wait ${!}
done

echo "Getting certificate..."
echo "DOMAIN is set to: $DOMAIN"
echo "EMAIL is set to: $EMAIL"

certbot certonly \
    --staging \
    --webroot \
    --webroot-path "/vol/www/" \
    -d "$DOMAIN" \
    --email "$EMAIL" \
    --rsa-key-size 4096 \
    --agree-tos \
    --noninteractive
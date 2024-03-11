#!/bin/bash

set -e

echo "Checking for dhparams.pem"
if [ ! -f "/vol/proxy/ssl-dhparams.pem" ]; then
  echo "dhparams does not exist - creating it"
  openssl dhparam -out /vol/proxy/ssl-dhparams.pem 2048
fi

# Avoid replacing these with envsubst
export host=\$host
export request_uri=\$request_uri

echo "Checking for fullchain.pem"
if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
  echo "No SSL cert, enabling HTTP only..."
  # Ensure the path here matches where your template files are stored
  envsubst < /etc/nginx/templates/default.conf.tpl > /etc/nginx/conf.d/default.conf
else
  echo "SSL cert exists, enabling HTTPS"
  # Ensure the path here matches where your template files are stored
  envsubst < /etc/nginx/templates/default-ssl.conf.tpl > /etc/nginx/conf.d/default.conf
fi

# Prevents NGINX from running in background. This way all logs are piped to Docker logs
nginx -g 'daemon off;'
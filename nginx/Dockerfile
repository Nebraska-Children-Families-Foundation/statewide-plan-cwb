FROM nginx:alpine

# Create the templates directory
RUN mkdir -p /etc/nginx/templates

# Copy the template files into the templates directory
COPY nginx/default.conf.tpl /etc/nginx/templates/
COPY nginx/default-ssl.conf.tpl /etc/nginx/templates/

# Copy other Nginx configuration files
COPY nginx/options-ssl-nginx.conf /etc/nginx/conf.d/

# Copy the run script
COPY run.sh /run.sh

ENV APP_HOST=app
ENV APP_PORT=9000

RUN apk --no-cache add openssl bash
RUN chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

CMD ["./run.sh"]
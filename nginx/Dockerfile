FROM owasp/modsecurity-crs:nginx-alpine

USER root

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Create the log directory for ModSecurity logs
RUN mkdir -p /var/log/nginx && \
    touch /var/log/nginx/modsec_debug.log && \
    chown nginx:nginx /var/log/nginx /var/log/nginx/modsec_debug.log

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/

# Copy SSL certificates
COPY certs/selfsigned.crt /etc/nginx/certs/selfsigned.crt
COPY certs/selfsigned.key /etc/nginx/certs/selfsigned.key

# Copy ModSecurity configuration
COPY custom-modsecurity.conf /etc/modsecurity.d/custom-modsecurity.conf

# Set permissions for SSL certificates
RUN chmod 644 /etc/nginx/certs/selfsigned.key && \
    chmod 644 /etc/nginx/certs/selfsigned.crt && \
    chown nginx:nginx /etc/nginx/certs/selfsigned.key /etc/nginx/certs/selfsigned.crt

USER nginx

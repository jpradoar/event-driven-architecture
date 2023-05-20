# FROM php:7.4-apache
# COPY ./www /var/www/html

FROM php:7.4-apache

# Copia el archivo docker-php-ext-enable
COPY docker-php-ext-enable /usr/local/bin/

# Instala las dependencias y habilita pdo_mysql
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        && docker-php-ext-install \
            pdo_mysql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia tu código PHP y archivos necesarios
#COPY index.php /var/www/html/index.php
COPY ./www /var/www/html
#COPY it-infrastructure-icon-28.jpg /var/www/html/it-infrastructure-icon-28.jpg

# Configuración adicional de Apache si es necesario

CMD ["apache2-foreground"]
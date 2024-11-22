FROM php:8.3.14-apache-bookworm

RUN echo "extension=pdo_mysql" >> /usr/local/etc/php/php.ini-production && docker-php-ext-install pdo_mysql
#COPY php.ini /usr/local/etc/php/php.ini
COPY ./www /var/www/html


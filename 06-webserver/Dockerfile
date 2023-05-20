FROM php:7.1-apache

RUN apt-get -y update && apt-get -y install --fix-missing curl apt-utils zlib1g-dev libicu-dev  libfreetype6-dev libjpeg62-turbo-dev libsqlite3-dev libsqlite3-0 libmcrypt-dev

# Install xdebug
RUN pecl install xdebug-2.5.0 && \
docker-php-ext-install mcrypt pdo_mysql mysqli gd tokenizer json -j$(nproc) intl mbstring && \
docker-php-ext-enable xdebug mysqli && \
docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ 
ADD ./php.ini /usr/local/etc/php/php.ini
ADD ./www/* /var/www/html/

# Enable apache modules
RUN a2enmod rewrite headers
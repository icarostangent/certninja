FROM wordpress:latest

RUN pecl install redis && docker-php-ext-enable redis
RUN curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
COPY wp-cli.phar /usr/local/bin/wp

# RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
# RUN php composer-setup.php --install-dir=/usr/local/bin --filename=composer
# RUN php -r "unlink('composer-setup.php');"

# RUN composer require stripe/stripe-php
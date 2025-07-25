# php-app/Dockerfile
FROM php:8.2-cli
WORKDIR /app

# Install git and unzip, which are required by Composer
RUN apt-get update && apt-get install -y git unzip

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

COPY composer.json .
RUN composer install --no-dev --optimize-autoloader

COPY index.php .
CMD ["php", "index.php"]

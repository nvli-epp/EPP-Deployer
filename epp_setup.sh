#Database Installation and Import EPP Database

export DEBIAN_FRONTEND="noninteractive"

echo "Set root user password for database"
read pass
echo "Enter Databses name for Emienent Personality Portal"
read dbname

sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password $pass"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $pass"
sudo apt-get update
sudo apt-get -y install mysql-server

echo "Creating eminentpp database"
mysql -uroot -p$pass -e "CREATE DATABASE $dbname;"

echo "Importing the database on Mysql server"
mysql -uroot -p$pass $dbname < eppdb.sql

#Apache and Php packages installation
sudo apt-get install apache2 -y
sudo apt-get install php7.0 -y
sudo apt-get install php7.0-mysql php7.0-xml php7.0-gd php7.0-mbstring libapache2-mod-php7.0 snmp libsnmp-dev zip unzip php7.0-fpm php7.0-cli php7.0-curl nfs-common curl -y

# Apache Server configuration
cd /etc/php/7.0/apache2/
sudo sed -i -e 's/allow_url_fopen = On/allow_url_fopen = Off/g' php.ini
sudo a2enmod rewrite
sudo service apache2 restart
cd $HOME
sudo sed -i '12,12 s/^/#/' /etc/apache2/sites-enabled/000-default.conf
sudo sed -i '13i\        DocumentRoot /var/www/eminentpp/docroot' /etc/apache2/sites-enabled/000-default.conf

sudo sed -i '15i\        <Directory /var/www/eminentpp/docroot>'  /etc/apache2/sites-enabled/000-default.conf
sudo sed -i '16i\             AllowOverride All                '  /etc/apache2/sites-enabled/000-default.conf
sudo sed -i '17i\        </Directory>'  /etc/apache2/sites-enabled/000-default.conf



#!/bin/bash

##Download and place codebase on Server
cd $HOME
wget https://github.com/nvli-epp/EPP-Deployer/archive/master.zip
unzip master.zip
sudo mkdir /var/www/eminentpp
cd $HOME/EPP-Deployer-master
sudo cp ./docroot.tar.gz /var/www/eminentpp/
cd /var/www/eminentpp/
sudo tar -xzvf docroot.tar.gz
sudo rm -rf docroot.tar.gz
sudo chown -R www-data:www-data /var/www/eminentpp/docroot/*

## Database configuration in settings.php file
#db_name=eminentpp
#db_pass=root
db_admin=root
sudo find /var/www/eminentpp/docroot/sites/default/settings.php -type f -exec sed -i "s/dbname/${dbname}/g" {} \;
sudo find /var/www/eminentpp/docroot/sites/default/settings.php -type f -exec sed -i "s/dbadmin/${db_admin}/g" {} \;
sudo find /var/www/eminentpp/docroot/sites/default/settings.php -type f -exec sed -i "s/dbpass/${pass}/g" {} \;








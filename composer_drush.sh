cd $HOME
#sudo apt-get install curl
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
mkdir drush
cd drush
composer require drush/drush:8
sudo sed -i "94i\alias drush8='$HOME/drush/vendor/bin/drush'"  ~/.bashrc
cd
#source ~/.bashrc 
source ~/.bashrc


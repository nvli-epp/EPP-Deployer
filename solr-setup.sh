# Solr set up for EPP portal
sudo apt-get update && apt-get upgrade -y
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:webupd8team/java
#Press [ENTER] when requested. Now, you can install the latest version of Java 8 with apt-get.
#Update the package lists to fetch the available packages from the new PPA
sudo apt-get update
sudo apt-get install oracle-java8-installer
#Press Y to continue and agree to the license by clicking on the OK button.	
cd /opt
sudo wget https://archive.apache.org/dist/lucene/solr/6.2.0/solr-6.2.0.tgz
sudo tar -xzf solr-6.2.0.tgz solr-6.2.0/bin/install_solr_service.sh --strip-components=2
sudo bash ./install_solr_service.sh solr-6.2.0.tgz
sudo service solr start
sudo su - solr -c "/opt/solr/bin/solr create -c eminent_production -n data_driven_schema_configs"
#Note: <eminent_production> is name of the solr core. User is free to choose any name for solr core.
#sudo su - solr -c "mkdir /var/solr/data/eminent_production/conf"
sudo su - solr -c "cp /var/www/eminentpp/docroot/modules/contrib/search_api_solr/solr-conf/6.x/* /var/solr/data/eminent_production/conf"




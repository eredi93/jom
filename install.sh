#!/bin/bash

usage()
{
cat << EOF
usage: $0 options

OPTIONS:
   -h      Show this message
   -d      Set project directory. Default 'pwd'.
   -l      Set PostgreSQL Listen address. Default '*'.
   -u      Set PostgreSQL Admin User. Default 'root'.
   -p      Set PostgreSQL Admin User Password. Default 'root'.
   -a      Set host PostgreSQL Admin User. Default '0.0.0.0/0'.
EOF
}

PROJECT_DIR=
LISTEN_ADDRESS=
USER=
PASSWD=
ADDRESS=

while getopts "h:d:l:u:p:a:" OPTION; do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         d)
             PROJECT_DIR=$OPTARG
             ;;
         l)
             LISTEN_ADDRESS=$OPTARG
             ;;
         u)
             USER=$OPTARG
             ;;
         p)
             PASSWD=$OPTARG
             ;;
         a)
             ADDRESS=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

if [[ -z $PROJECT_DIR ]]
then
     echo "$(tput setaf 1)Project directory has not been passed. Using $PROJECT_DIR$(tput sgr0)"
     exit 1
fi

if [[ -z $LISTEN_ADDRESS ]]
then
     LISTEN_ADDRESS='*'
     echo "$(tput setaf 1)PostgreSQL Listen_address has not been passed. Using $LISTEN_ADDRES$(tput sgr0)"
fi

if [[ -z $USER ]]
then
     USER='root'
     echo "$(tput setaf 1)PostgreSQL admin user has not been passed. Using $USER$(tput sgr0)"
fi

if [[ -z $PASSWD ]]
then
     PASSWD='root'
     echo "$(tput setaf 1)PostgreSQL admin user password has not been passed. Using $PASSWD$(tput sgr0)"
fi

if [[ -z $ADDRESS ]]
then
     ADDRESS='0.0.0.0/0'
     echo "$(tput setaf 1)PostgreSQL admin user host has not been passed. Using $ADDRESS$(tput sgr0)"
fi


sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get autoremove -y

sudo apt-get install -y vim curl libffi-dev libpq-dev openvpn postgresql postgresql-contrib nginx python-setuptools python3 python3-pip mcrypt git

sudo pip3 install virtualenv

sudo -u postgres createuser $USER --superuser
sudo sed -i "/host    all             all             127.0.0.1\/32            md5/ a\
	host    all             $USER             $ADDRESS            md5" /etc/postgresql/9.3/main/pg_hba.conf

sudo sed -i "s/^#listen_addresses = 'localhost'/listen_addresses = '$LISTEN_ADDRESS'/g" /etc/postgresql/9.3/main/postgresql.conf
sudo -u postgres createdb jom
sudo -u postgres psql -U postgres -d postgres -c "alter user $USER with password '$PASSWD';"
sudo service postgresql restart

sudo echo "server {
    listen 80;
    root $PROJECT_DIR/public;
    index index.php;
    server_name jom;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/run/jom.pid;
    }

}" > /etc/nginx/sites-available/jom

ln -s /etc/nginx/sites-available/jom /etc/nginx/sites-enabled/jom
sudo rm /etc/nginx/sites-enabled/default

sudo sed -i "s/sendfile on;/sendfile off;/g" /etc/nginx/nginx.conf

sudo service nginx restart

sudo echo "description \"uWSGI server instance configured to serve Jom application\"

start on runlevel [2345]
stop on runlevel [!2345]

start on started postgresql

script
    . $PROJECT_DIR/env/bin/activate
    cd $PROJECT_DIR
    exec uwsgi --ini uwsgi.ini
end script" > /etc/init/jom.conf

if [ -f "$PROJECT_DIR/env" ]
then
    sudo rm -rf $PROJECT_DIR/env
fi

if [ -f "/home/vagrant/.bashrc" ]
then
    echo "cd $PROJECT_DIR" >> /home/vagrant/.bashrc
fi

cd $PROJECT_DIR && virtualenv env && source env/bin/activate && pip install -r requirements.txt

sudo service nginx restart

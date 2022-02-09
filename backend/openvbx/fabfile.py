"""
openVBX
for installation doc https://github.com/twilio/OpenVBX/blob/master/INSTALL.markdown
https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-in-ubuntu-16-04
"""

from fabric.api import *

env.hosts = ['ubuntu@ec2-54-88-129-214.compute-1.amazonaws.com', ]
env.user = 'ubuntu'
env.key_filename = '../.local/keys/duopaleo.pem'

base_user = 'root'
base_user_pass = 'Icandothis2335$'
db_name = 'OpenVBX_db'
db_user = 'OpenVBXdbuser'
db_user_pass = 'Icandothis2335$'


@task
def deploy():
    check_updates()
    step0_install_reqs()
    install_db()
    create_db()

    step1_download_Openvbx()

    install_optional_software()
    config()
    restart_apache()


@task
def check_updates():
    sudo('apt-get update ')
    sudo('apt-get upgrade -y ')


@task
def step0_install_reqs():
    sudo("apt install -y apache2 libapache2-mod-php git "
         "php php-mcrypt php-mysql php-curl php-mbstring php-simplexml"
         "sendmail sendmail-bin")


@task
def install_db():
    sudo(f"debconf-set-selections <<< 'mysql-server mysql-server/root_password password {base_user_pass}'")
    sudo(f"debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password {base_user_pass}'")
    sudo('apt-get install -y  mysql-server')
    # mysql  Ver 14.14 Distrib 5.5.50, for debian-linux-gnu (x86_64) using readline 6.3
    sudo('mysql --version')
    sudo('echo -e "{0}\nn\n\n\n\n\n " | mysql_secure_installation'.format(base_user_pass))


@task
def create_db():
    x = "CREATE DATABASE {0}; GRANT ALL PRIVILEGES ON {0}.* TO {1}@localhost IDENTIFIED BY '{2}'; FLUSH PRIVILEGES".format(
        db_name, db_user, db_user_pass)
    run('echo  "{0}"| mysql -u {1} -p{2}'.format(x, base_user, base_user_pass))


@task
def install_optional_software():
    # sudo("apt-get install -y  php-memcache")
    # sudo("apt-get install -y  memcached")
    # sudo('apt-get -y install php7.0-opcache php-apcu')
    sudo('apt-get -y install phpmyadmin')


@task
def update_webroot_dir():
    sudo('rm -rd /var/www/html')
    sudo('usermod -a -G www-data ubuntu')
    sudo('chown -R root:www-data /var/www/')
    sudo('chmod -R g+w /var/www/')


@task
def step1_download_Openvbx():
    run('git clone git@github.com:twilio/OpenVBX.git /var/www/')


@task
def config():
    sudo('chmod 777 -Rf /var/www/OpenVBX/config')
    sudo('chmod 777 -Rf /var/www/audio-uploads')


@task
def restart_apache():
    sudo('systemctl restart apache2')


@task
def install_removed_php7_mysql_functions():
    "openvbx doesn't detect the mysql because it was only supporting php5.6"
    # https://ckon.wordpress.com/2015/08/06/put-mysql-functions-back-into-php-7/
    sudo('mkdir ext')
    with cd('ext'):
        sudo('git clone https://github.com/php/pecl-database-mysql mysql --recursive')
    with cd('ext/mysql'):
        sudo('apt install php7.0-dev')
        run('phpize')
        run('./configure')
        run('make')
        run('make install')
        # open /etc/php/7.0/apach2/php.ini and extension
        # /usr/lib/php/20151012/mysql.so

# after installing all these requirements, go to url and follow the steps there
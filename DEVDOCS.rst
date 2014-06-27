

Developer Documentation
=================

Get .pem key for WCV

ssh in with the pemfile

create a new user

add to the appropriate group

create .ssh directory with authorized_keys file (add your id_rsa.pub key in here)

make sure permissions are right on your .ssh dir

give passwordless sudo:
USE VISUDO FOR THIS

USERNAME   ALL = (ALL) NOPASSWD:ALL

add your public ssh key to the wildlife user's authorized_keys file so you can ssh in directly as that user


sudo apt-get install git
sudo apt-get install python-pip
sudo apt-get install python-dev


# only install on the server
sudo apt-get install nginx
sudo apt-get install python-pip python-dev build-essential
sudo apt-get install libmysqlclient-dev
sudo apt-get install mysql-server

install virtualenv, virtualenvwrapper

create user and grant privileges
create auctionmanager database

run schema migration
./manage.py syncdb
(create super user at your discretion)


add a sites-available/[name-you-want-for-application] file



    server {
        listen   80;
        server_name wildlife;
        # no security problem here, since / is alway passed to upstream
        root /home/wildlife/website/auction-manager-online/auctionmanageronline;
        # serve directly - analogous for static/staticfiles
        location /static {
            # this changes depending on your python version
            autoindex on;
            alias /home/wildlife/website/auction-manager-online/staticfiles/;
        }
        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_connect_timeout 10;
            proxy_read_timeout 10;
            proxy_pass http://localhost:8000/;
        }
        # what to serve if upstream is not available or crashes
        error_page 500 502 503 504 /media/50x.html;
    }


run gunicorn in the background (from the project root) Nginx should pick up the changes. you can test to see if you have
gunicorn installed correctly by running """ gunicorn auctionmanager.wsgi:application """.  If you see information
printed to the console, it's working. If it's not, something's not right.


(wildlife)wildlife@wcv-auction:~/website/auction-manager-online$ echo_supervisord_conf > supervisord.conf

Add the following entry to the supervisord.conf file (located in the project root dir OR /etc/supervisord.conf)

[program:wildlife]
command = /home/wildlife/.virtualenvs/wildlife/bin/gunicorn auctionmanageronline.wsgi:application
user = wildlife


run supervisord, which should give you access to the supervisorctl command
add the wildlife host to your .ssh/config file with forward agent set to yes. if not sure how to do this, GIYF



To run this locally, you'll need to set an environment variable "DEBUG" (and "TEMPLATE_DEBUG") to TRUE. In Linux, you can do this
by typing in your terminal window "export DEBUG=True && export TEMPLATE_DEBUG=True"

To make those changes permanent, open your ~/.bashrc file and add
"""
export DEBUG=True
export TEMPLATE_DEBUG=True
"""
to the file. close it, and run "source ~/.bashrc"

That will reload your bash profile and you should be able to run django locally with no configuration changes



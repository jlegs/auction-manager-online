Auction Manager Online
===============

This Web application aims to help nonprofits manage their auction fundraisers, which often constitute a large portion of their annual funding.

Setup
---------------
pip install MySQL-python
pip install South
pip install django-multiselectfield
pip install django-extensions
pip install werkzeug


create database auctionmanager;
create user 'amo'@'localhost' identified by 'password';
grant all on auctionmanager.* to 'amo'@'localhost';



Secret Key
---------------
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#secret-key
make sure we do this before deploying this for production





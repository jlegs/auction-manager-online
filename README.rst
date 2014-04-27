Auction Manager Online
===============

For any nontechnical readers who got here through some sort of search for 'auction manager', this web app is currently under development and not ready for deployment.

The application aims to help nonprofits manage auction fundraisers, which often constitute a large portion of their annual funding.

Currently, the system allows users to create auction Items, Guests and Invoices (which default to one invoice per guest).

Users can also view the list of guests, items and invoices, as well as view invoices and guests by table assignment.

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





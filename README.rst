Auction Manager Online
===============

For any nontechnical readers who got here through some sort of search for 'auction manager', this web app is currently under development and not ready for deployment.

The application aims to help nonprofits manage auction fundraisers, which often constitute a large portion of their annual funding.

Current features:

* Add guests (invoice is created for the guest when the guest is created)

* Add auction items

* Add invoices (in case you need to just create a new invoice for a guest)

* Merge multiple invoices into one

* View Guest list (or view the guest list per table)

* View Invoice list (or view the invoices for guests at a specific table)

* Search Invoices by Bidder number, first name or last name

* View Item list

.. image::(https://github.com/lightcastle/auction-manager-online/blob/screenshots/auction.png "Auction ScreenShot")


Setup
---------------
To run this locally, you'll need Django 1.6 and a mysql server running. You'll need several Python dependencies. Pip is the best tool to do this. You can get that by installing it via the commandline:

	sudo apt-get install python-pip

You'll also need virtualenv. (We also recommend virtualenvwrapper to make your life easier). We'll install these globally so you can use them elsewhere.

	sudo pip install virtualenv

	sudo pip install virtualenvwrapper

Next we'll create our virtualenv for the project. This can be any name you'd like, since this will be specific to your development environment.

	mkvirtualenv [virtualenv-name-of-your-choosing]

Once you've created that, you can activate the virtual environment through "workon" or "deactivate", plus the name of the virtual environment you created.

Now you can install all the needed dependencies with a quick and simple

	pip install -r requirements.txt

The last thing you should need to do is make sure your database is ready. The following commands (entered inside a running MySQL shell) should get you  up and running.

	create database auctionmanager;

	create user 'amo'@'localhost' identified by 'password';
	
	grant all on auctionmanager.* to 'amo'@'localhost';

Don't forget to sync your database using ./manage.py syncdb before running your first migrations!

Now you can run the Django server and visit localhost:8000 to see the app in action!



Secret Key
---------------
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#secret-key
make sure we do this before deploying this for production





import os

# AIRBNB_ENV is set to dev on local machine and prod on server
env = os.environ.get('AIRBNB_ENV')

if env == 'development':
	# sets up development environment
	DEBUG = True
	HOST = 'localhost'
	PORT = 3333
	DATABASE = {
		'host': '158.69.85.16',
		'user': 'airbnb_user_dev',
		'database': 'airbnb_dev',
		'port': 3306,
		'charset': 'utf8',
		'password': os.environ.get('AIRBNB_DATABASE_PWD_DEV')
	}

if env == 'production':
	# sets up production environment
	DEBUG = False
	HOST = '0.0.0.0'
	PORT = 3000
	DATABASE = {
		'host': '158.69.85.16',
		'user': 'airbnb_user_prod',
		'database': 'airbnb_prod',
		'port': 3306,
		'charset': 'utf8',
		'password': os.environ.get('AIRBNB_DATABASE_PWD_PROD')
	}

if env == 'test':
	#sets up testing environment
	DEBUG = False
	HOST = 'localhost'
	PORT = 5555
	DATABASE = {
		'host': '158.69.85.16',
		'user': 'airbnb_user_test',
		'database': 'airbnb_test',
		'port': 3306,
		'charset': 'utf8',
		'password': os.environ.get('AIRBNB_DATABASE_PWD_TEST')
	}
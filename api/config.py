import os

if os.environ.get('AIRBNB_ENV') == 'development':
	# sets up development environment
	DEBUG = True
	HOST = 'localhost'
	PORT = 3333
	DATABASE = {
		'host': '54.183.231.35',
		'user': 'airbnb_user_dev',
		'database': 'airbnb_dev',
		'port': 3306,
		'charset': 'utf8',
		'password': os.environ.get('AIRBNB_DATABASE_PWD_DEV')
	}

if os.environ.get('AIRBNB_ENV') == 'production':
	# sets up production environment
	DEBUG = False
	HOST = '0.0.0.0'
	PORT = 3000
	DATABASE = {
		'host': 'localhost',
		'user': 'airbnb_user_prod',
		'database': 'airbnb_prod',
		'port': 3306,
		'charset': 'utf8',
		'password': os.environ.get('AIRBNB_DATABASE_PWD_PROD')
	}

if os.environ.get('AIRBNB_ENV') == 'test':
	#sets up testing environment
	DEBUG = False
	HOST = 'localhost'
	PORT = 5555
	DATABASE = {
		'host': '54.183.231.35',
		'user': 'airbnb_user_test',
		'database': 'airbnb_test',
		'port': 3306,
		'charset': 'utf8',
		'password': os.environ.get('AIRBNB_DATABASE_PWD_TEST')
	}
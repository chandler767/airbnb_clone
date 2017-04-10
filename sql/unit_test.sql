CREATE USER 'airbnb_user_test'@'%'
	IDENTIFIED BY 'airbnbtest';

CREATE DATABASE airbnb_test
	DEFAULT CHARACTER SET utf8
	DEFAULT COLLATE utf8_general_ci;

GRANT ALL PRIVILEGES
	ON airbnb_test.*
	TO 'airbnb_user_test'@'%'
	IDENTIFIED BY 'airbnbtest';
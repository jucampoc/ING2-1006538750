CREATE DATABASE IF NOT EXISTS `hospital_patients`;
CREATE DATABASE IF NOT EXISTS `api_gateway`;
GRANT ALL PRIVILEGES ON `hospital_patients`.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON `api_gateway`.* TO 'root'@'%';
FLUSH PRIVILEGES;
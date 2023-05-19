-- Adminer 4.8.1 MySQL 5.5.5-10.9.4-MariaDB-1:10.9.4+maria~ubu2204 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `clients`;
CREATE DATABASE `clients` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `clients`;

DROP TABLE IF EXISTS `clients`;
CREATE TABLE `clients` (
  `id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `client` varchar(50) NOT NULL,
  `archtype` varchar(20) NOT NULL,
  `hardware` varchar(20) NOT NULL,
  `xdate` varchar(20) NULL,
  `license` varchar(20) NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=ascii COLLATE=ascii_general_ci;



DROP DATABASE IF EXISTS `users`;
CREATE DATABASE `users` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `users`;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id_usuario` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=ascii COLLATE=ascii_general_ci;

-- 2022-12-29 17:18:06